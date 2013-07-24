Doctrine and Domain Events
==========================

I have written about the `Domain Event Pattern
</2012/08/25/decoupling_applications_with_domain_events.html>`_ before and want
to focus on this pattern again by explaining its integration into the Doctrine
ORM on a very technical level.

The Domain Event Pattern allows to attach events to entities and dispatch them
to event listeners only when the transaction of the entity was successfully
executed. This has several benefits over traditional event dispatching
approaches:

- Puts focus on the behavior in the domain and what changes the domain
  triggers.
- Promotes decoupling in a very simple way
- No reference to the event dispatcher and all the listeners required except in
  the Doctrine UnitOfWork.
- No need to use unexplicit Doctrine Lifecycle events that are triggered on all
  update operations.

This block post will introduce a very simple implementation for Domain Events
with Doctrine2. You should be able to easily extend it to be more flexible,
reliable or optionally even asynchronuous. I skip some of the glue code in this blog post,
but you can try the full code by checking out `this Gist
<https://gist.github.com/beberlei/53cd6580d87b1f5cd9ca>`_ and running
``composer install`` and then ``php domain_events.php``.

Lets look at the following entity, an ``InventoryItem`` tracking the number
we have this item in stock:

.. code-block:: php

    <?php
    namespace MyProject\Domain;

    use Doctrine\ORM\Mapping as ORM;
    use MyProject\DomainSuperTypes\AggregateRoot;

    /**
     * @Entity
     */
    class InventoryItem extends AggregateRoot
    {
        /**
         * @Id @GeneratedValue @Column(type="integer")
         */
        private $id;
        /**
         * @Column
         */
        private $name;
        /**
         * @Column(type="integer")
         */
        private $counter = 0;

        public function __construct($name)
        {
            $this->name = $name;
            $this->raise('InventoryItemCreated', array('name' => $name));
        }

        public function checkIn($count)
        {
            $this->counter += $count;
            $this->raise('ItemsCheckedIntoInventory', array('count' => $count));
        }
    }

We want this entity to raise two domain events using the ``raise($eventName,
array $properties)`` method.  Our preferred use case for this code looks like this:

.. code-block:: php

    <?php
    $item = new InventoryItem('Cookies');
    $item->checkIn(10);

    $entityManager->persist($item);
    $entityManager->flush(); // fire events here

One or many listeners should react to the events being fired, for example print their contents to the screen:

.. code-block:: php

    <?php
    class EchoInventoryListener
    {
        public function onInventoryItemCreated($event)
        {
            printf("New item created with name %s\n", $event->name);
        }

        public function onItemsCheckedIntoInventory($event)
        {
            printf("There were %d new items checked into inventory\n", $event->count);
        }
    }

As the first building block, we need a `Layer Supertype
<http://martinfowler.com/eaaCatalog/layerSupertype.html>`_ for our entities,
called ``AggregateRoot`` adding the event raising capabilities to all entities that need it:

.. code-block:: php

    <?php
    namespace MyProject\DomainSuperTypes;

    abstract class AggregateRoot
    {
        private $events = array();

        public function popEvents()
        {
            $events = $this->events;
            $this->events = array();

            return $events;
        }

        protected function raise($eventName, array $properties)
        {
            $this->events[] = new DomainEvent($eventName, $properties);
        }
    }

This class allows us to add events to an entity using ``raise()`` as we have
seen in the ``InventoryItem`` entity before.

Now we need Doctrine to process the events during a transaction (``flush()``).
We do this by keeping all entities with domain events, and then triggering
the domain events after the transaction has completed. This is a vital part
of the domain events pattern, because it guarantees every listener that the
state leading to the event is already in the database.

Technically we implement this with a Doctrine EventListener that listeners for
the ``postFlush``, ``postPersist``, ``postUpdate`` and ``postRemove`` events:

.. code-block:: php

    <?php
    namespace MyProject\DomainEvents;

    use Doctrine\ORM\EntityManager;
    use MyProject\DomainSuperTypes\AggregateRoot;

    class DomainEventListener
    {
        private $entities = array();

        public function postPersist($event)
        {
            $this->keepAggregateRoots($event);
        }

        public function postUpdate($event)
        {
            $this->keepAggregateRoots($event);
        }

        public function postRemove($event)
        {
            $this->keepAggregateRoots($event);
        }

        public function postFlush($event)
        {
            $entityManager = $event->getEntityManager();
            $evm = $entityManager->getEventManager();

            foreach ($this->entities as $entity) {
                $class = $entityManager->getClassMetadata(get_class($entity));

                foreach ($entity->popEvents() as $event) {
                    $event->setAggregate($class->name, $class->getSingleIdReflectionProperty()->getValue($entity));
                    $evm->dispatchEvent("on" . $event->getName(), $event);
                }
            }
            $this->entities = array();
        }

        private function keepAggregateRoots($event)
        {
            $entity = $event->getEntity();

            if (!($entity instanceof AggregateRoot)) {
                return;
            }

            $this->entities[] = $entity;
        }
    }

Now we only need to put this code together with Doctrine to get it working:

.. code-block:: php

    <?php
    $evm = new EventManager();
    $evm->addEventListener(
        array('postInsert', 'postUpdate', 'postRemove', 'postFlush'),
        new DomainEventListener()
    );
    $evm->addEventListener(
        array('onInventoryItemCreated', 'onItemsCheckedIntoInventory'),
        new EchoInventoryListener
    );
    $conn = array(/* data */);
    $config = new Configuration();
    $entityManager = EntityManager::create($conn, $config, $evm);

Now the example from above, creating and checking in inventory items
will trigger the ``EchoInventoryListener`` and print the data to the screen.

This example is very simple but shows how you can incorporate Domain Events into
your Doctrine projects. The following improvements can be made if necessary:

- Use a base EventSubscriber for the Domain Listeners, that automatically
  registers all the domain event listener methods. This way you don't have
  to manually list them when calling ``$evm->addListener()``.

- Implement one class for every domain event, allowing to typehint the events
  in listeners, with much more helpful information about the contained data.

- If you prefer asynchroneous processing, serialize the events into a
  `domain_events` table instead of triggering the events directly.
  Add a daemon to your project that tails the table and triggers the events
  in the background.

I hope this blog post helps you when considering to use Domain Events Pattern with
Doctrine. Again, `see the code on this Gist
<https://gist.github.com/beberlei/53cd6580d87b1f5cd9ca>`_ for a working example.

.. author:: default
.. categories:: PHP
.. tags:: PHP, Doctrine, DomainEvents, Patterns
.. comments::
