Bounded Contexts
================

I regularly fall into the same trap when building applications: Trying to find
the one model that unifies all the use-cases and allows to solve every problem.
From discussions with other developers I know not to be the only one making this
mistake.

It is propably a human trait trying to find the one line that connects
every dot. However in software design there is a case to be made for the
separation of contexts to tackle complexity. Eric Evans described this in detail with the
`"Bounded Context" <http://dddcommunity.org/uncategorized/bounded-context/>`_ pattern in his
"Domain-Driven Design" book. According to an interview with Evans I read
somewhere, he considers it one of the most important patterns in the whole book.

The essence of this strategic pattern is to embrance the separation of
different parts of an application and develop different models as different
domain contexts. Consistency and constraints are enforced within one context,
but don't necessarily hold in another context.

The goal is simplication and freeing us from the burden of finding that one
model that fits all use cases. It is much less awkward to have some parts of
the model reimplemented for different purposes than creating God objects that
try to unify everything, and failing at this task.

Evans goes even further and introduces a significant amount of patterns
that describe the relationship between different bounded contexts.

An Experiment
-------------

At the `SoCraTes conference <http://www.socrates-conference.de/>`_ in August
last year, I participated in a DDD architecture game by `Cyrille Martraire
<https://twitter.com/cyriux>`_ that focused on distilling bounded contexts. We
were given a very simple domain concept "Customer" and assigned different roles
in the business.

Everyone described their perfect customer very differently, imagining the
Customer object that fits all these requirements was quite an eye opener. Even
if there is no such single software that operates a business, going to the
extreme and defining 10 different angles for a single concept made me clear,
that sometimes different overlapping implementations are not such a bad thing.

Problems and Solutions
----------------------

One problem when applying bounded contexts is data synchronization.
Synchronization between contexts can be reached in many different ways,
three of which are:

1. The `Domain Event
   <http://martinfowler.com/eaaDev/DomainEvent.html>`_ pattern that integrates
   nicelly into Domain-Driven Design and simplifies the synchronization with
   other parts of an application.
   
2. Correlation Ids of the same entity into the different contexts and a clean
   seperation of the data (no shared data necessary).

3. Another way are immutable read models (value objects) of the data managed in
   another context (entity).

In any way relying on `Eventual
Consistency <http://en.wikipedia.org/wiki/Eventual_consistency>`_ helps
solving the synchronization problem.

Depending on how your bounded contexts seperate from each other, duplication of
classes is necessary as well. This is something that has to be accounted for
and you should make sure that only one context is responsible for changing the
same data. Different contexts can have different behaviors on the same data.
This is actually a point where Domain-Driven Design and `Data, Context and
Interaction (DCI)
<http://www.whitewashing.de/2012/08/16/oop_business_applications__data__context__interaction.html>`_
intersect.

Conclusion
----------

Applying bounded contexts to an application or a cluster of applications helps
developers and domain experts to focus on problems in their specific context.
Sometimes each context even has its own domain-expert. The benefit for
developers is a simplified abstraction of different parts of the modelled
problem.

.. author:: default
.. categories:: none
.. tags:: ApplicationDesign
.. comments::
