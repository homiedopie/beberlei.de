Doctrine and SOLID
==================

I often get asked how you can use `Doctrine2
<http://www.doctrine-project.org>`_ and implement `the SOLID principles
<http://en.wikipedia.org/wiki/SOLID_(object-oriented_design)>`_ at the same
time. It bugs me having to reply: It is not really possible.  Because Doctrine2
does not support value-objects (or embedded-objects), it is very hard to pull
the `Single Responsibility Principle
<http://en.wikipedia.org/wiki/Single_responsibility_principle>`_ off.

These problems are related to the inability to share behavioral code through
aggregation and the complexity of state transformations. Combining both, your
average entity with 5-15 fields can end up with hundrets or thousands lines of
code. The solutions to both problems boil down to `minimizing duplication and
maximizing clarity
<http://www.jbrains.ca/permalink/the-four-elements-of-simple-design>`_.

Extracting Value Objects: Minimize Duplication
----------------------------------------------

Entity classes responsibility here are the state transformations of their
internal fields.  This can simply be done by using setter methods or `with real
code, when avoiding setters
<http://whitewashing.de/2012/08/22/building_an_object_model__no_setters_allowed.html>`_.
These state transformations can be part of different responsibilities,
specificially when properties belong to different groups of concepts.

Take a very simple entity that contains updated/created at logic:

.. code-block:: php

    <?php
    use Doctrine\ORM\Mapping as ORM;

    /**
     * @ORM\Entity
     * @ORM\HasLifecycleCallbacks
     **/
    class Person
    {
        /**
         * @ORM\Column(type="datetime")
         **/
        private $createdAt;
        /**
         * @ORM\Column(type="datetime")
         **/
        private $updatedAt;

        public function __construct()
        {
            $this->createdAt = new \DateTime("now");
            $this->updatedAt = new \DateTime("now");
        }

        /**
         * @ORM\PreUpdate
         **/
        public function updatedAt()
        {
            $this->updatedAt = new \DateTime("now");
        }
    }

If you want to duplicate this logic to another second entity, then in Doctrine
the solution for this is using traits. `Kore
<http://kore-nordmann.de/blog.html>`_ will dismiss this solution, because
traits create a hard dependency. Even if we accept the static dependency,
traits are not perfect even for this very simple example, because its very
likely that you cannot override the constructor of every entity.

The solution is to extract a value object ``Timestamped`` that contains
all the logic:

.. code-block:: php

    <?php
    class Timestamped
    {
        private $createdAt;
        private $updatedAt;

        public function __construct()
        {
            $this->createdAt = new \DateTime("now");
            $this->updatedAt = new \DateTime("now");
        }

        public function updatedAt()
        {
            $this->updatedAt = new \DateTime("now");
        }
    }

    class Person
    {
        private $timestamped;

        public function __construct()
        {
            $this->timestamped = new Timestamped();
        }
    }

See how all the code could be moved into ``Timestamped`` and is now reusable
in other entities.

Doctrine has no support for embedded objects, which is very sad. I am working
very hard to get this feature into Doctrine as soon as possible.

Extract Method Objects: Maximizing clarity
------------------------------------------

Once you have identified groups of fields that are modified, then the
complexity of the state transformations can attract lots of code.

Take an ``Order`` object that has a method for calculating the shipping costs,
depending all the order items and products.
To seperate calculations from state transformations you can extract
method objects instead of inlining the code into the ``Order`` object.

For this kind of extraction I create a folder ``Order`` and put all
the extracted method objects in the ``Order`` subnamespace.

.. code-block:: php

    <?php
    namespace MyProject\Entity {

        class Order
        {
            public function calculateShippingCosts()
            {
                $calculator = new ShippingCostCalculator();
                $this->shippingCosts = $calculator->calculate($this);
            }
        }
    }

    namespace MyProject\Entity\Order {

        class ShippingCostCalculator
        {
            public function calculate(Order $order)
            {
                return 0;
            }
        }
    }

From this step its easy to make the code reusable by passing the shipping cost
calculator:

.. code-block:: php

    <?php
    class Order
    {
        public function calculateShippingCosts(ShippingCostCalculator $calculator)
        {
            $this->shippingCosts = $calculator->calculate($this);
        }
    }

Another benefit is that you can test the shipping cost calculator directly in a
unit-test and avoid checking for the correctness indirectly through a getter
method for the shipping costs.

Conclusion
----------

Not all the techniques to implement SOLID code can be exploited when using Doctrine
for technical reasons. In the future I hope to support value objects in
Doctrine to make this possible.


.. author:: default
.. categories:: php
.. tags:: php
.. comments::
