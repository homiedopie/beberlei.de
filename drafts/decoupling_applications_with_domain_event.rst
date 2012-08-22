Decoupling applications with Domains Events
===========================================

In the `previous posts
<http://whitewashing.de/2012/08/18/oop_business_applications__command_query_responsibility_seggregation.html>`_
I have described 3 architectural patterns for business applications. Applying
them to your software helps you decouple the business logic from the
application/framework/UI. However given sufficient complexity, you will want to
decouple different parts of your business model from each other as well.

As an example, lets think of a batch process in your application that updates
orders from a CRM or logistics system:

- You receive an XML with full users and order representations
- You need to update certain user fields
- You need to update certain order fields
- Some orders require creating accounts in different remote systems
- If the user has not confirmed his email yet he should receive an opt-in
  mail instead.
- If the user confirms his opt-in mail, all outstanding remote accounts are
  created.

You can build all the steps into a single batch processing service. This will
be a particularly huge service and in violation of the Single Responsibility
principle. 

the part with updating of users and fields has nothing to with the sending of
mails and creation of remote accounts.  We want to decouple them from each
other.

The first obvious choice is to decouple them into distinct services:

- Import Service
- Authentication Service
- Account Generation Service

All these services have dependencies on infrastructure objects, database,
mailer and so on. We could inject the authentication and account generation
services into the Import Service, but with rising complexity this will lead to
a lasagna of services and the execution path will dig deep into this and this
is not nearly as tasty as eating real lasagna.

::

    ImportService
    |_AuthenticationService
    | |_Mailer
    | |_Database
    |_AccountGenerationService
    | |_Database
    | \_RemoteFacade
    \_Database

This becomes more complicated when transaction semantics need to be taken care
of. For example dependencies between mailer and database services.

What we want instead is a sequential execution of those nested services, but
only if the parent service executed successfully:

:: 

    ImportService
    \_Database

    AuthenticationService
    |_Mailer
    \_Database

    AccountGenerationService
    |_Database
    \_RemoteFacade

We could use an event dispatcher in all of the services to notify each other,
but the `DomainEvent pattern
<http://martinfowler.com/eaaDev/DomainEvent.html>`_ does this more subtle:
Every entity is an event provider and can emit events. Whenever a transaction
is committed and an operation is completed, we take all the events emitted from
all entities (looking at the identity map for example) and trigger observing
event handlers.

.. code-block:: php

    <?php

    class Order
    {
        use EventProvider;

        public function importData(array $data)
        {
            // 1. do something with $data

            // 2. raise event
            $this->raise(new OrderImportCompleted(array("data" => $data)));
        }
    }

The Event provider trait aggregates all the events, and offers
and API for external services to pull them from the entity:

.. code-block:: php

    <?php
    trait EventProvider implements EventProviderInterface
    {
        private $emittedEvents = array();

        protected function raise(DomainEvent Event)
        {
            $event->getMessageHeader()->setEntity($this);
            $this->emittedEvents[] = $event;
        }

        public function dequeueEmittedEvents()
        {
            $events = $this->emittedEvents;
            $this->emittedEvents = array();
            return $events;
        }
    }

Our infrastructure must then trigger event handlers, based
on the event names. We want the following command/event chain to happen:

- Command executes
- Entities emit events
- Command transaction succeeds
- Events trigger event handlers
- Event handlers execute more commands
- Restart from 1.

With this approach we can decouple all services from each other and avoid
deep nesting in each other. Yet we still have transactional dependencies,
by dropping all events when the parent command fails. Transactions over
multiple commands will not have ACID properties though, instead you will have
to look into `BASE transactions <http://queue.acm.org/detail.cfm?id=1394128>`_
that are important in systems with eventual consistency. This is one downside
that you need to take into account.

The Domain Event pattern is a prerequisite for full blown `CQRS
<http://queue.acm.org/detail.cfm?id=1394128>`_. My `LiteCQRS
<https://github.com/beberlei/litecqrs-php>`_ library includes a simple
implementation of DomainEvent and EventProvider classes and integration into
Symfony and Doctrine ORM. Generally this pattern is very easy to implement
though, so that you can just have a look at the implementation and take the
best parts for your own.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
