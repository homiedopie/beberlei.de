Doctrine and DomainEvents
=========================

I have written about the `Domain Event Pattern
</2012/08/25/decoupling_applications_with_domain_events.html>`_ before and want
to focus on this pattern again by explaining its integration into the Doctrine
ORM.

The DomainEvent Pattern allows to attach events to entities and dispatch them
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

As the first building block, we need a `Layer Superclass` for our entities,
adding the event raising capabilities to all entities that need it:

.. code-block:: php

    <?php

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
