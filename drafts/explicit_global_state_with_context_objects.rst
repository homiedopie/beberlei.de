Explicit Global State with Context Objects
==========================================

Global State is considered bad for maintainability of software. Side effects on
global state can cause a very nasty class of bugs. Context objects are one
flavour of global state. For example, I remember that Symfony1 had a
particularly nasty context object that was a global singleton containing
references to very many services of the framework.

As with every concept in programming, there are no absolute truths though and
there are many use-cases where context objects make sense. This blog posts
tries to explain my reasons for using context objects.

What is a Context?
------------------

Context is defined as all the information and circumstances in which
something can be *fully* understood. In daily programming this is mostly
related to the state of variables and databases. Some examples in the world
of PHP include the superglobals ``$_GET`` and ``$_POST``.

Any piece of code is always running in some context and the question is how much
of it is explicit in the code and how much is hidden.

A context object is a way to make the existing context explicit for your code.

Context Objects
---------------

Lets take a look at the Definition of a context object::

    A context object encapsulates the references/pointers to services and
    configuration information used/needed by other objects. It allows the objects
    living within a context to see the outside world. Objects living in a different
    context see a different view of the outside world.

Besides the obvoius use of encapsulating services and config variables, the
definition talks about two important properties:

1. Allows to see the outside world, does not mean it can change it.
   In my opinion it is essential that context objects are immutable,
   to avoid problems of side effects.   

2. The possibility of objects living in different contexts, seeing
   different context objects suggets that a context object
   should never be a singleton.

By using objects instead of global variables for context, we can use
encapsulation to achieve immutability.

Context Object Examples
-----------------------

As mentioned before, Request variables are one context that exists in your
applications.  Introducing explicit context objects for them will yield
considerable benefits over using the superglobals.

In Symfony2 the ``Request`` is a context object that explicitly wrapts ``$_GET``,
``$_POST`` and other superglobals. It is almost immutable (except attributes)
and it is not a singleton. The way the Symfony2 Request works it even allows to
create sub-contexts by creating new request objects.

The Session object in Symfony2 can be exchanged with other implementations
that run without ``$_SESSION``. Ever tried to run tests, workers or console
tools with code that uses the PHP session? An abstraction implemented
as a context object as Symfony provides allows different sessions in the
same php process and would theoretically allow you to enforce immutability
(not by default).

Application Context
-------------------


.. author:: default
.. categories:: none
.. tags:: none
.. comments::
