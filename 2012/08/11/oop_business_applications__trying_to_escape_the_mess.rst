OOP Business Applications: Trying to escape the mess
====================================================

.. note::

    tl;dr Version: I present a list of problems with OOP business applications from
    my personal experience and then introduce 3 approaches that I was put in
    contact with over the last year, DCI, EBI and CQRS. This post is an
    introduction to a series about this approaches.

I always mentally divide the world of programming into two large parts:

1. Library and system programming
2. business applications
   
The first produces code solving technical problems, often in a beautiful and
dedicated way. The second regularly produces mess, hopefully still
serving customers by optimizing their business. This differentation an
exageration, but from my experience its far easier to run a greenfield business
project into the ground than a new library.

There has to be a reason why so many programmers dedicate much free time to
open source projects. It might be empirical prove, that all our business
projects don't make us happy at the end of the day and we have to show
ourselves that we can do better.

I enjoy writing business applications much more, but they are also much more
difficult to get right in both social and technical dimensions.  One
motivational driver of `my open source activities
<https://github.com/beberlei>`_ always was to simplify the technical dimension
of OOP business applications.

My Personal List of Annoyances
------------------------------

This blog post is not about blaming customers (the usual suspect), its about
finding the problems in usual OOP code of business systems from my experience
with PHP projects. To keep things short, I will list my *personal* list of annoyances
in business projects in no particular order. These are highly subjective
points.

- Getter/Setter Madness of Objects that are used to store data into
  databases. Leading to huge objects that are essentially just meaningless
  stores of data.
- Updating complex object graphs from user input.
- Seperation of model, controller and views, especially when dealing with
  forms. This is very complicated to achieve.
- Lazy Loading and Query performance problems when using an ORM. Additionally
  replacing parts of the views with hand-crafted SQL is often difficult and/or
  time intensive, when already using an ORM.
- Inability to decouple code that was written with CRUD (generators and
  utilities) in mind towards more domain driven code, when the requirements
  change.
- Dependency mess leading to hard to test code, generally leading to untested
  applications. Generally frameworks create huge dependencies that
  make your domain model messy.
- Focus on synchroneous request/response handling makes later usage of message
  queues very complicated and expensive to refactor towards.
- Tight coupling of model against the framework code.
- Junior developers have too much freedom, when there is not much structure in
  the code, but rather just a big ball of mud. Additionally with the tight
  coupling of so many components, junior developers get easily lost in the code
  and produce unexpected side-effects. 
- Use-cases easily span more than 5 classes. To grasp the interaction you have
  to keep lots of code in your head.
- Constant violations of `SOLID
  <http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29>`_ principles
  due to framework or persistence requirements.
- Compared to library development, user-facing applications often have much
  higher coupling between classes and namespaces. In libraries its often easy
  to find different concerns, but in applications they seem hard to divide for
  developers.
- In combination with a rich javascript client, requirements to update objects
  through their CRUD API produces concurrency and lost-update hell, that
  dynamic server-side applications could mostly avoid before.

Essentially if you work in a tight schedule, project based environment where
the decision makers sell rapid application development and prototyping, then you
often have only one, maybe one and a half attempts to get the big picture
right. From that moment on you have to build on that decision and hope for the
best.

We have tried not to go the RAD+CRUD tools ways in several projects, to escape
the problems listed above. But without changes in your mindest you end up with
hand written mess, compared to getting there with tools.

Specifically `Domain Driven Design
<http://en.wikipedia.org/wiki/Domain-driven_design>`_ applied naively can make
the problem even worse. It easily leads to lasagna code, where you have layers
of layers that are very hard to understand. Personally I prefer spagetthi code
over lasagna code, because its comparatively easy to understand.

Finding new Approaches
----------------------

Rather than to embrace the suck and dive deeper into CRUD architectures, I felt
there has to be some solution to organize business models structurely to avoid
all (or most) of these problems. In the PHP world with `Symfony2
<http://www.symfony.com>`_ and `Doctrine2 <http://www.doctrine-project.org>`
you have a powerful toolbox to avoid many of the problems above, but it is
still not simple to write clean object oriented applications.

After years of participation in both projects I still feel there is a missing
puzzle piece, to reach a clean seperation of all the model concers from
framework and persistence. 

Thanks to `Gordon <https://twitter.com/go_oh>`_, `Stefan
<https://twitter.com/spriebsch>`_ and `Thomas <https://twitter.com/tom_noise>`_
I was introduced to several "new" approaches to OO application design that I
started to explore in the past last months. They are:

- `Data, Context, Interaction (DCI)
  <http://en.wikipedia.org/wiki/Data,_context_and_interaction>`_ - which Gordon
  studied alot
- `Entity, Boundary, Interactor (EBI)
  <http://alistair.cockburn.us/Hexagonal+architecture>`_, also called Hexagonal
  architecture or "Ports and adapters". Gained popularity after `Uncle Bobs talk
  at Ruby Midwest
  <http://www.confreaks.com/videos/759-rubymidwest2011-keynote-architecture-the-lost-years>`_
  last year.
- `Command-Query-Responsibility-Segregation (CQRS)
  <http://en.wikipedia.org/wiki/Command-query_separation>`_ well described in a
  `blost post by Udi Dahan
  <http://www.udidahan.com/2009/12/09/clarified-cqrs/>`_ and in a hands on `one
  day video class <http://www.viddler.com/v/dc528842>`_ by Greg Young.

I am not sure if you can group them under a common category, but they are
neither just patterns nor software architectures. All three approaches make you
think about application development beyond just "service layers" in radically
new ways. All three have helped me rethink business applications in different
ways. 

In the next weeks I will talk about each of these approaches individually, show
some examples and then wrap up my thoughts about all of them.

.. note::

    Gordon and I will talk about this topic on the `Free and Open Source
    Conference <http://www.froscon.de/en/home/>`_ in Sankt Augustin Germany on
    25th/26th August of 2012. Feel free to drop by and discuss this topic!

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
