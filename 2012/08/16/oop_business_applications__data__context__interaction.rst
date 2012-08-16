OOP Business Applications: Data, Context, Interaction
=====================================================

Other posts in this series:

- `OOP Business Aplications: Trying to escape the
  mess <http://whitewashing.de/2012/08/11/oop_business_applications__trying_to_escape_the_mess.html>`_
- `OOP Business Applications: Entity, Boundary, Interactor
  <http://whitewashing.de/2012/08/13/oop_business_applications_entity_boundary_interactor.html>`_


The next design pattern for technical system design is called "Data, Context,
Interaction". It's inventors Trygve Reenskaug and James Coplien call it a new
paradigm, in the context of PHPs langugage constraints it can be classified as
architectural design pattern. I came accross this pattern through `Gordon Oheim
<https://twitter.com/go_oh>`_. He has also invested quite some time going
through the book on DCI and trying to understand this pattern with me.

As in the EBI pattern, DCI seperates data objects (Data) from behavior implemented
in use-cases (Context). Data objects are never directly involved in these
use-cases, but are "casted" to their respective roles that they are taking in
the use-case. This can be implemented with aggregation or traits in PHP.

One goal of DCI is to get object-oriented programming to a place, where you
can look at a use-case and its roles and be very sure that the programm is
running correctly, because you can guarantee that there are no unexpected side
effects. It also aims at keeping the amound of code required to keep in mind
for a given use-case as small as possible, allowing developers to reason about
the code with more confidence.

Terminology
-----------

In DCI, **data** are objects that encapsulate the state of the application.
As in EBI, they only contain logic that is true for all the possible use-cases. 
These classes represent *what the system is*.

**Roles** and **Context** represent *what the system does* and are supposed to
capture the End User's Mental Model as close as possible.

**Roles** add behavior to the data objects by either wrapping them or
acting as traits for the data objects.

**Context** is the use-case and fulfils its role by making roles **interact** with
each other. These roles then modify the underlying data.

Example
-------

Starting from the bank account example of the EBI post, we can introduce DCI 
quite easily by adding the missing concept of roles. In the use case of
transfering money that would be:

* TransferMoneySource
* TransferMoneySink (Destination)

We can do this by either introducing two interfaces and two concrete
implementations that accept the ``BankAccount`` as object to work on
or by building two traits. I will go down the route with traits, to show
one possible use-case for this new PHP 5.4 feature. The idea here is to
implement all the behavior necessary on a trait and then have simple dummy
objects using them in the tests for this use-case.

.. code-block:: php

    <?php
    trait TransferMoneySource
    {
        public function transferTo($destination, Money $money)
        {
            $destination->transferFrom($destination, $money);  
        }
        abstract public function withdraw(Money $money);
    }
    trait TransferMoneySink
    {
        public function transferFrom($source, Money $money)
        {
            $source->withdraw($money);
            $this->desposit($money);
        }
        abstract public function deposit(Money $money);
    }

Any checks for balances, credit limits or other things would also happen
here. The ``withdraw`` and ``deposit``  on the data objects should be as
dumb as possible, so that their implementation does not cause any side-effects
on the execution of this use-case.

The bank account would then be modified to look:

.. code-block:: php

    <?php

    class BankAccount
    {
        use TransferMoneySource, TransferMoneySink;

        private $balance;

        public function __construct()
        {
            $this->balance = new Money(0);
        }

        public function withdraw(Money $money)
        {
            $this->balance = $this->balance->subtract($money);
        }

        public function deposit(Money $money)
        {
            $this->balance = $this->balance->add($money);
        }
    }

The use-case ``TransferMoney`` would then be modified to create Roles instead
of Data objects from the DAO. This can be a bit tricky when you have multiple
data objects implementing the same role and you have no way of knowing which
underyling data object to pick. The binding of data objects to roles happens
in the use-case. The use-case needs a means to retrieve objects with certain
roles, which then access underlying data sources. To avoid that your use-cases
have to know about how to bind roles to data, you could use GUIDs in your
application and fetch all objects from one data store. Another way would be to
implement data access objects for roles, that then know how to retrieve their
corresponding data.


.. code-block:: php

    <?php
    class MoneyTransfer
    {
        private $source;
        private $destination;

        public function __construct($moneySource, $moneySink) 
        {
            $this->source = $moneySource;
            $this->destination = $moneySink;
        }

        public function transferMoney(Money $money)
        {
            $this->source->transferTo($this->destination);
        }
    }

The simplicity of this is appealing, however don't forget that we have
abstracted I/O completley here. There has to be code that deals with that part
of the system somewhere. However this again is not at the heart of all the DCI
examples out there, making it difficult to reason about the actual practical
implications.

.. note::

    One drawback with this example is, that PHP does not support typehinting for
    traits.

Here is an example of how the bank application service could look like:

.. code-block:: php

    <?php
    class BankApplicationService
    {
        public function transferMoney($sourceId, $destinationId, Money $amount)
        {
            $source      = $this->objectStorage->find($sourceId);
            $destination = $this->objectStorage->find($destinationId);

            $useCase = new MoneyTransfer($source, $destination);

            $conn = $this->conn->beginTransaction();

            try {
                $result = $useCase->transferMoney($amount);
                $conn->commit();

                return $result;
            } catch(\Exception $e) {
                $conn->rollback();
            }
        }
    }

The ``ObjectStorage`` here is a service (repository) that can find any
persistent data object by a global ID. This is necessary, because it
doesn't actually matter what data object uses the necessary traits
for this use-case.

Again as in EBI, in a bigger system you would need to find some abstraction
layer that does this in a more generic way.

Conclusion
----------

When Gordon started showing me this pattern we were both puzzled as how
to actually implement this in the real world. Especially the concept
of binding roles to data objects still confuses us. Most notably why the use
of traits or aggregates should actually constitute a new programming paradigm
instead of just another way to do OOP.

In Scala casting data objects to roles is actually possible by binding traits
to objects at runtime. This is not possible in PHP however and has to be done
statically.

Compared to EBI, DCI focuses drastically on transaction script domain logic, by
suggesting to implement roles for every use-case for the sake of avoiding
side-effects. This is actually is very valuable lesson from this pattern.
Finding means to decrease the complexity of software is always a good thing.
And the explicit definition of this concept as **roles** is actually easy to
explain to other programmers. 

One thing that is lacking in DCI is that there is no concrete mechanism to deal
with the boundary to other parts of the system. This is actually a step back
from EBI and I suggest using EBI pattern in combination with DCI to solve this.

The largest benefit from DCI (and its self proclaimed goal) is the mapping from
the users/customers mental model directly into the code by using Use-Cases and
Roles. The communication with the customer about behavior can exclusively focus
on the current context and its use-case. Mapping this behavior to actual data
can then be done in a different step.

This simplification of use-cases and reduction of side-effects between
different parts of the system has other benefits: It can lead to easier to test
code and makes it much easier for developers to develop on small and isolated
parts of the system.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
