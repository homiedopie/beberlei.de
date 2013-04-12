Traits are Static Access
========================

In a Twitter discussion yesterday I formulated my negative opinion
about traits and Matthew asked me to clarify it:

.. image:: http://www.whitewashing.de/images/traits_are_static_access.png

I used to look forward to traits as a feature in PHP 5.4, but after discussions
with `Kore <http://twitter.com/koredn>`_ I came to the conclusion that traits
are nothing else than static access in disguise. They actually lead to the
exact same code smells. 

Let's step back and take a look at the code smells that Static code produces:

- Tight coupling, no way to exchange at runtime
- Not mockable
- Static code cannot be overwritten through inheritance
- Global state (increases likelihood of unwanted side effects)

This blog post shows that Traits actually have the first three problems
themselves and exhibit the same code smells. But they even have some additional
problems on their own:

- Not testable in isolation
- Theoretically stateless, but not enforced in PHP
- Traits can have very high impact on the code base

Take the following code, which tries to implement reusable
controller code through traits:

.. code-block:: php

    <?php
    class MyController
    {
        use Redirector;

        protected $container;

        public function __construct($container)
        {
            $this->container = $container;
        }

        public function someAction()
        {
            return $this->redirect("route_xyz", array());
        }
    }

    trait Redirector
    {
        public function redirect($routeName, $parameters)
        {
            return new RedirectResponse(
                $this->generateUrl($routeName, $parameters)
            );
        }

        public function generateUrl($routeName, $parameters)
        {
            return $this->container->get('router')->generateUrl(
                $routeName,
                $parameters
            );
        }
    }

Lets spot the problems:

1. ``Redirector`` is tightly coupled to ``MyController``. There is no way to
   change this during runtime, by using a different type of redirector, it has
   to be exactly the trait used at compile time. This is exactly what static
   access enforces as well.

2. The trait accesses ``$this->container`` without defining it and couples itself against
   the implementing classes. We can actually refactor this to include an
   abstract method ``getContainer()`` in the trait. But if we have multiple
   traits now, all having a ``getContainer()`` method then we run into method
   class problems that cannot be solved. We could pass the container as an
   argument to the method, but that actually defeats the purpose of the
   abstraction here.

   Traits using state of their "parents" usually create bidirectional
   coupling between classes, something which should be avoided for good
   software design.

3. No way to overwrite subset of functionality. If I want to use only one
   method of a trait and a second one slighty different, then I cannot
   overwrite this function of ``Redirector`` for example in ``MyController``.

4. I cannot mock the traits functionality, therefore I cannot test
   ``MyController`` as a unit only in combination with a trait.

5. I cannot test the trait as a unit, I always have to create a class
   that uses the trait to be able to write a test for it.
   This prevents me from testing traits in isolation.

6. Once you start using ``Redirector`` in many controllers, its impact
   on your code base (see `Code Rank
   <http://pdepend.org/documentation/software-metrics/index.html>`_) increases
   a lot. Traits are concrete implementations and therefore violate the
   Dependency Inversion SOLID principle: Changes in the trait require adoptions
   in all the implementing classes.
   
   With aggregation you could depend on an abstraction ``Redirector`` or
   turn it into an abstraction in the moment that you need different
   functionality.

The discovery of this properties of traits me to the conclusion that traits are
just static access in disguise.

To see this argument a bit more drastically, you can "rewrite" a PHP 5.4 trait
into "pseudo" static code:

.. code-block:: php

    <?php
    class MyController
    {
        public $container;

        public function __construct($container)
        {
            $this->container = $container;
        }

        public function someAction()
        {
            return Redirector::redirect("route_xyz", array());
        }
    }

    class Redirector
    {
        public function redirect($routeName, $parameters)
        {
            return new RedirectResponse(
                self::generateUrl($routeName, $parameters)
            );
        }

        public function generateUrl($routeName, $parameters)
        {
            return $this->container->get('router')->generateUrl(
                $routeName,
                $parameters
            );
        }
    }

Calling dynamic methods statically actually works right now (and access to
``$this`` of the parent class will luckily be removed in PHP 5.5). Let's
reformulate it into something that is actually using static methods and
will work on 5.5, requires changes to the visibility of properties though:

.. code-block:: php

    <?php
    class MyController
    {
        public $container;

        public function __construct($container)
        {
            $this->container = $container;
        }

        public function someAction()
        {
            return Redirector::redirect($this, "route_xyz", array());
        }
    }

    class Redirector
    {
        public static function redirect($thiz, $routeName, $parameters)
        {
            return new RedirectResponse(
                self::generateUrl($thiz, $routeName, $parameters)
            );
        }

        public static function generateUrl($thiz, $routeName, $parameters)
        {
            return $thiz->container->get('router')->generateUrl(
                $routeName,
                $parameters
            );
        }
    }

Can you see the familiarity? If Traits can be rewritten as calls to static methods,
how can they be any better than static methods? They exhibit the exact same
problems and produce the same code smells.

Conclusion: Traits should be avoided at all costs, just like static methods.

Rule of Thumb: If you want to use a trait, try to think how to solve the
problem with aggregation.

If you want to read more about problems with traits,
`Anthony <http://blog.ircmaxell.com/2011/07/are-traits-new-eval.html>`_ wrote
about them quite a while ago.

.. author:: default
.. categories:: PHP
.. tags:: PHP
.. comments::
