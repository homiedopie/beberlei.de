Modelling Bulk Changes
======================

Bulk changes are write operations that affect hundrets, thousands or even
millions of records and usually require very efficient code to be processed in
an acceptable amount of time. Typical examples here are imports of data from
third-party systems into your own database or mass workflow operations such as
Jira's bulk change for tickets.

Implementing bulk changes often poses a significant risk for a good application
design, because regularly applications are built on top of database abstractions or ORMs
that are not primarily built with batch processing in mind.
The results of having batch operations mixed into a applications with
CRUD-focused database abstraction layers can be:

- a very slow system using only the database abstraction
- a duplication of lots of business logic in a CRUD and a bulk part of the app
- an inconsistent, mixed system of both abstraction and optimized code

All three outcomes are bad from a design perspective, because they don't scale
or they completly break encapsulation and mix optimized code with business
logic in endless spagetthi code.  As one of the authors of Doctrine2 I have
seen this in my own projects, but also in many customers projects.

If requirements for bulk changes are known from the beginning, explicitly
modelling them leads to much better code. It may even allow both single item
(CRUD) operations and batch operations to use exactly the same object-oriented
code-base without performance penalties.

Take the issue tracker example from the first paragraph: We need to design
a system that allows users to change the status of tickets in bulk, with
power users having an estimated number of 100.000 tickets. If we would use
Doctrine ORM to model a ``Ticket`` entity as a domain object then we are
already screwed, fetching all the ticket data into memory and then saving
it again is very slow.

Instead lets model change, for example transitioning the ticket from "open"
to "resolved" status: 

.. code-block:: php

    <?php

    class TransitionChange
    {
        /** @var int */
        private $ticketId;
        /** @var int */
        private $newStatusId;

        public function __construct(int $ticketId, int $newStatusId)
        {
            $this->ticketId = $ticketId;
            $this->newStatusId = $newStatusId;
        }
    }

Collecting a list of transition changes is much cheaper than collecting
the actual ticket entities with all their data and assocations and we
can use another explicit object modelling the bulk change:

.. code-block:: php

    <?php

    class ChangeTickets
    {
        private $changes = array();

        public function transitionStatus(int $ticketId, int $newStatusId)
        {
            $this->changes[] = new TransitionChange($ticketId, $newStatusId);
        }

        public function getChanges()
        {
            return $this->changes;
        }
    }

If we had other tpyes of changes (Change Assignee, Move to next Sprint, Add fix
version, ...) we could add them here as well.

Saving each change is a matter of writing a repository/gateway for the
``ChangeTickets`` object that evaluates **all** changes to perform efficient bulk write
operations that the database supports, for example a set of ``UPDATE ... WHERE ... IN``
queries for similar changes to multiple tickets.

.. code-block:: php

    <?php

    class ChangeTicketsDbalGateway implements ChangeTicketsGateway
    {
        /** @var \Doctrine\DBAL\Connection */
        private $connection;

        public function bulk(ChangeTickets $changeTickets)
        {
            $this->beginTransaction();

            try {
                // assume its only TransitionChange here, group/partition here when more changes exist
                $transitionChanges = $changeTickets->getChanges();
                $this->performTransitionStatusChange($transitionChanges);

                $this->connection->commit();
            } catch (\Exception $e) {
                $this->connection->rollBack();
                throw $e;
            }
        }

        protected function performTransitionStatusChange(array $changes)
        {
            $newStatuses = array();
            foreach ($changes as $change) {
                $newStatuses[$change->getNewStatusId()][] = $change->getTicketId();
            }

            foreach ($newStatuses as $newStatusId => $ticketIds) {
                // simplification (optimization with batches of up to $n ticketIds might be necessary)
                $sql = 'UPDATE ticket SET status = ? WHERE id IN (' .  implode(', ', $ticketIds) . ')';
                $this->connection->exceuteUpdate($sql, array($newStatusId));
            }
        }
    }

This is a very simple first implementation, but it ignores some important constraints:

- Tickets may not change to any arbitrary status, the workflow enforces specific transitions.
- Ticket transitions may depend on the user who is performing them.

There are multiple ways to implement these requirements:

1. In the database queries, by enhancing the ``UPDATE`` query to enforce the
   rules. This path is quick but leads to the dark side. It is the most simple
   and performant way, but offers no good way to give feedback to the user which
   changes were rejected and for what reasons. It only makes sense if you
   want to swallow rejected changes silently. A sample query for our status transition
   might look like this:

    .. code-block:: php

        <?php

        $allowedFromStatusIds = $this->findStatusIdsAllowedToTransitionTo($newStatusId);

        $sql = 'UPDATE ticket
                   SET status = ?
                 WHERE id IN (' .  implode(', ', $ticketIds) . ')
                   AND status IN (' . implode(', ', $allowedFromStatusIds) . ')';
        $actuallyChanged = $this->connection->exceuteUpdate($sql, array($newStatusId));

2. Calling a ``filter()`` method inside ``ChangeTicketsGateway#bulk()`` that
   returns a new ``ChangeTickets`` with only valid changes. This method allows
   to implement the filtering efficiently by performing batch SQL operations,
   but hides and mixes this logic with the low-level database operations.
   To allow notifing the user which changes were applied you can return
   the filtered Changes from the bulk operation:

    .. code-block:: php

        <?php

        $changes = new ChangeTickets();
        $changes->transitionStatus(1, 2);
        //...

        $appliedChanges = $changeTicketsGateway->bulk($changes);

   One variant of this is turning ``ChangeTicketsGateway#filter()`` into a public
   method and explicitly performing the operation before calling ``bulk()``.
   The API is more dangerous because you can forget to call filter,
   but it allows you to compile better information about rejected changes:

    .. code-block:: php

        <?php

        $changes = new ChangeTickets();
        $changes->transitionStatus(1, 2);
        //...

        $validChanges = $changeTicketsGateway->filter($changes);
        $changeTicketsGateway->bulk($validChanges);

   This approach leads to considerable logic stored in database/infrastructure
   classes, but there are alot of cases where this is perfectly valid.

3. In ``ChangeTickets#transitionStatus()`` method by filtering for allowed transitions.
   This requires passing a service into ``ChangeTickets`` that can perform the
   operation ``isAllowed($change)`` efficiently:

    .. code-block:: php

        <?php

        class ChangeTickets
        {
            /** @var ChangeTicketsGateway */
            private $changeTicketsGateway;

            public function transitionStatus(int $ticketId, int $newStatusId)
            {
                $this->apply(new TransitionChange($ticketId, $newStatusId));
            }

            protected function apply($change)
            {
                if (!$this->changeTicketsGateway->isAllowed($change)) {
                    return;
                }
                $this->changes[] = $change;
            }
        }
    
   This is better than solutions one and two, because it moves some of the
   logic from database/infrastructure class towards a domain class
   ``ChangeTickets``, preventing accidental saving of invalid changes.
   
   But honestly this is just very little logic in the domain class, we are
   relying alot on the database here to enforce our business rules. Only the
   database knows the allowed transitions, it knows the state of the ticket and
   then checks for validity.

4. To avoid hiding rules inside the database and still ending up with efficient
   code a careful refactoring is necessary to move more logic into
   ``ChangeTickets``. There is probably more than one solution to this problem
   

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
