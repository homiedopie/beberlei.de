OOP Business Applications: Command-Query-Responsibility-Seggregation (CQRS)
===========================================================================

The last pattern for desigining your business logic is called
"Command-Query-Responsiblity-Seggregation" or short CQRS. It has its roots in
the `"Command Query Seperation"
<http://en.wikipedia.org/wiki/Command-query_separation>`_ principle that was
put forward by Bertrand Meyer.

Wikipedia has a very good summary about what this principle is about:

::

    Command-Query-Seperation states that every method should either be a
    command that performs an action, or a query that returns data to the
    caller, but not both. In other words, asking a question should not change
    the answer. More formally, methods should return a value only if they are
    referentially transparent and hence possess no side effects. 

CQRS is an OOP design pattern building on that imperative principle. As
I tried to understand this pattern I found that there are many different
variations of it that all have their place. This however makes it hard to write an
introduction blog post, without confusing the reader or selling CQRS as a
complexity nightmare, which is not always the case.

The first obvious requirement: Our write service methods are not allowed to
return data anymore. This may increase the complexity at first, especially when
you work with MySQL that only generates IDs during the INSERT operation,
however a strict adherence to this principle allows us to turn every command
from synchroneous to asynchroneous processing later without much problems.
This solves one problem of my list of annoyances in a clean way ("Never return
data from your commands").

At its heart there is obviously the seperation of Read and Write methods. This
can be easily achieved by just having two different service layer classes
instead of one. This insight alone is not really helpful, its just moving
methods around. Coupled to this change however is the notion, that read and
write models don't have to be the same. Let me clarify what problems of my list
occur, just because of using the same models and DTOs for reading and writing:

- Getter/Setter Madness. In write models we don't need setters, as we can have
  methods that handle each command explicitly. Additionally in write scenarios
  we don't need all that bidirectional associations that make the use of an ORM
  much more difficult. In Read-only models we don't actually need
  getters/setters. They could just use public properties or even be arrays.
- ORM Performance, Lazy Loading and Query Restrictions: In a write scenario we
  mostly need queries by primary key, changing only a few set of objects. In
  read scenarios we often need complex joins and aggregations. Using just one
  model mapped with one ORM may lead to both read and write scenarios to affect
  each other negatively.
- Reading a DTO, modifying it on the client then writing its full
  representation back to the server leads to very tricky problems with
  validation and state-machines. If you pass the whole DTO for updating, the
  model actually never knows what the intent of the change was. This requires
  complex mapping of all property and association changes from the DTO to the
  entity object. This approach has lead to a class of security problems called
  "mass-assignment-vulnerability", where in a mass assignment from DTO to
  entity object, the client can change fields he is not allowed to.

As the first step, why not transform SQL directly to a view model in a highly
optimized way? There is no actual need to pass through boundary, service layer, data
access objects and translate back and forth just to read some data. This is a
simple concept, but it has huge implications. For a modelling purist that I
want to be, it gives me absolution that I don't have to come up with the one
model that fits all use-cases. Read and write operations are so fundamentally
different, that we shouldn't reject to use different models for
them mentally and in code.

One drawback is obviously a naive implementation doubles the amount of classes
and services to write. But there are simple shortcuts to avoid having to write
a full blown read-model:

- Mapping SQL to PHP arrays and stdClass objects through a simple gateway is
  very simple.
- If the write model fits the read use-cases, does not have performance
  requirements and is not the central object of your domain, but rather just a
  sidekick: Just reuse it. In Doctrine ORM for example you could
  re-use the model, but hydrate it only as arrays - saving the costly
  transformation to an object model.



.. author:: default
.. categories:: none
.. tags:: none
.. comments::
