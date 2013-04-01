Bounded Contexts
================

I regularly fall into the same trap with applications, by thinking of the one
model that unifies all the use-cases and allows to solve every problem. From
talking to other developers I know that I am not the only one making this
mistake.

It is propably a human trait, trying to find the one puzzle piece that
connects everything. However in software design there is a case to be made for
the separation of different contexts. Eric Evans described this in detail in
his `"Bounded Context" <http://domaindrivendesign.org/node/91/>`_ pattern in
Domain Driven Design. According to an interview with Evans I read, he considers
it the most important pattern in the whole book.

The essence of this strategic pattern is to embrance the separation of
different parts of an application and develop different models, when the parts
have different contexts. The goal is simplication and freeing us from the
burden of finding that one model that fits all use cases. Those different
application parts talk to each other through their public APIs, maybe even
seperated by a protocol such as HTTP.

We should remember this pattern more often when designing applications.

It is much less awkward to have some parts of the model reimplemented for
different purposes than creating God objects that try to unify everything,
and failing at this task..

One example of bounded context, is seperating the CRUD parts from the more
complicated and interesting parts that benefit from domain driven design, say
workflow on top of the data.

Instead of having an entity class (say the ``Customer``) that is used in both
the CRUD and the domain driven part of the application, have both parts
implement their own. Then you can actually `build a domain model without
getters and setters
<http://www.whitewashing.de/2012/08/22/building_an_object_model__no_setters_allowed.html>`_.

At the `SoCraTes conference <http://www.socrates-conference.de/>`_ that took place
in August last year, I participated in a DDD architecture game
that focused on distilling bounded contexts. We were
given a very simple domain concept "Customer" and assigned different roles in
the business.  Everyone described their perfect customer very differently,
imagining the Customer object that fits all these requirements was quite an eye
opener. Even if there is no such single software that operates a business,
going to the extreme and defining 10 different angles for a single concept made
me clear, that sometimes different overlapping implementations are not such a
bad thing.

One drawback of this approach might be duplication. Depending on how your bounded
contexts seperate from each other, this is something that has to be accounted
for. I think this is a solvable problem, depending entirely on how you
actually seperate the different contexts.

Another drawback might be necessary synchronization between contexts.  One way
to solve this in your application is the `Domain Event
<http://martinfowler.com/eaaDev/DomainEvent.html>`_ pattern that integrates
nicelly into Domain Driven Design and simplifies the synchronization with other
parts of an application. You can solve this by cleanly separating data of the 
same entity into the different contexts as well and using a correlation id
to connect them.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
