Spotting Feature Envy and Refactoring
=====================================

I was following `Aki's <http://twitter.com/rinkkasatiainen>`_ on the
`SoCraTes2014 <https://www.softwerkskammer.org/activities/socrates-2014>`_
conference last week about Legacy Code and Refactoring. In the session a piece
of real-world code was shown that contained one of most common code smells in
LegacyCode: Feature Envy.

Martin Fowler describes this smell as "a method that seems more interested in
a class other than the one it is in. The most common focus of the envy is the
data."

This code smell causes two very similar problems in a code base:

- Duplication of rules related to their data throughout the code base.
- Spreading domain concepts throughout the whole code-base.

A simple example can show this problem with ``DateTime`` is wide-spread in many
PHP projects. We often see code such as the following computation to
create a range of dates for a reporting function:

.. code-block:: php

    <?php

    function calculateReport(DateTime $start, $days)
    {
        if ($days < 0) {
            throw new InvalidArgumentException($days);
        }

        $endDate = clone $start;
        $endDate->modify('+' . $days . ' day');

        // calculation code here
    }

This is a really simple example for Feature Envy: The computation and
validation of creating an end date some days in the future of a start date
can easily be duplicated throughout the whole code base and implements
business rules that belong to the class ``DateTime`` itself:

.. code-block:: php

    <?php

    class DateTime
    {
        // ... other methods

        public function getDateDaysInFuture($days)
        {
            if ($days < 0) {
                throw new InvalidArgumentException($days);
            }

            $endDate = clone $this;
            $endDate->modify('+' . $days . ' day');

            return $endDate;
        }
    }

    function calculateReport(DateTime $start, $days)
    {
        $endDate = $start->getDateDaysInFuture($days);

        // calculation code here.
    }

(Note: You cant extend the builtin DateTime this way and need to subclass).

This is a great way to improve your code base massively and achieve what
Object-Oriented and Domain-Driven Design is about: Modelling concepts of the
domain by encapsulating data and behavior.

Learning to spot this kind of Feature Envy is a very good way to incrementally
improve your legacy code base towards better models. I find it very interesting
that the focus on fixing technical code-smells duplication and feature envy
actually leads to a better domain model. As a side effect it massively
deemphasizes DDD building blocks like Entity or Value Object, which in my
opinion are a big cause for confusion. Testability increases as well, because
data objects with behavior are much simpler to setup for testing.

That is why I recommend learning about Feature Envy. For me it is a very simple
approach to find improvements.

.. author:: default
.. categories:: none
.. tags:: CodeQuality
.. comments::
