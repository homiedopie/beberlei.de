CQRS and Traits
===============

If you apply CQRS and Domain Event pattern in a language that has traits, you can
share commands accross entities of multiple types. This is a very powerful
concept It might actually be comparable to **Roles** in the Data, Context,
Interaction paradigm.

Take for example the business requirement that managers have to double check
everything happening.

You could model this behavior as a trait:

.. code-block:: php

    <?php

    trait Approvable
    {
        private $approved = false;
        private $approvedBy;

        public function approve($managerName)
        {
            if ($this->approved) {
                throw new \RuntimeException("Already approved.");
            }

            $this->approved   = true;
            $this->approvedBy = $managerName;
        }
    }

Now you can have any approvable entity use this trait, for
example the hours worked by an employer on a particular project,
or the project offering to a customer:

.. code-block:: php

    <?php
    class HoursWorked
    {
        use Approvable;
    }
    class ProjectOffering
    {
        use Approvable;
    }

To use this behavior in a CQRS context, you would now create a command
and a corresponding command handler that manage the use-case of approving.
The example is using `LiteCQRS library
<https://github.com/beberlei/litecqrs-php>`_ which I put onto Github.

.. code-block:: php

    <?php
    use LiteCQRS\DefaultCommand;
    class ApproveCommand extends DefaultCommand
    {
        public $class; // necessary if $id is not a UUID
        public $id;
        public $username;
    }

    class ApprovalService
    {
        private $repository; // ctor omitted

        public function approve(ApproveCommand $command)
        {
            $resource = $this->repository->find($command->class, $command->id);
            $resource->approve($command->username);
        }
    }

And you got yourself some reusable business behavior, just have any Entity
implement the trait and you are good to go.

Lets rewrite the trait to make use of event-sourcing. Event Sourcing
means that every change of state in your domain model is triggered through an
event.

.. code-block:: php

    <?php
    use LiteCQRS\DefaultDomainEvent;

    class ManagementApprovedEvent extends DefaultDomainEvent
    {
        public $approvedBy;
    }

    trait Approvable
    {
        private $approved = false;
        private $approvedBy;

        public function approve($managerName)
        {
            if ($this->approved) {
                throw new \RuntimeException("Already approved.");
            }

            $this->approved   = true;
            $this->approvedBy = $event->approvedBy;

            $this->raise(new ManagementApprovedEvent(array(
                'approvedBy' => $managerName 
            )));
        }
    }

We introduced a new event ``ManagementApprovedEvent`` and use the ``apply()``
method of the LiteCQRS for Aggregate Roots. This introduces a loose dependency
from the Approvable trait to ``LiteCQRS\AggregateRoot``.

With this change now LiteCQRS will trigger the ``ManagementApprovedEvent``
and we can continue listening to the event and doing even more, decoupled
commands. For example we could compile a report of all the approved hours
worked and send it to somebody.

The possibility to implement these **Roles** with traits is infinite, and you can
just compose Entities as a set of **Roles**. For example these just came into
mind (or are variants of Propel behaviors):

- any reusable State Machines (Publishing, Workflows)
- Taggable (Add Tag, Remove Tag)
- AuthorizeRequired (Request, Confirm Authorization for an Entity using a Hash,
  with a particular timeframe where the authorization can be done)
- Participation (RequestParticipation, ConfirmParticipation, DenyParticipation)
- Translatable (Add Translation, Remove Translation)
- Commentable (Add Comment, Moderate Comment, Delete Comment)
- Geocodable (Set current Coordinates)
- CrudCreatable (Create from array)
- CrudEditable (Update from array)
- CrudDeletable (Delete)

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
