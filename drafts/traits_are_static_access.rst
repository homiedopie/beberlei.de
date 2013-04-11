Traits are Static Access
========================

I used to look forward to traits as a feature in PHP 5.4, but after
thinking about their use and discussions with `Kore <http://twitter.com/koredn>`_
I came to the conclusion that traits are nothing else than static access in
disguise and actually lead to the exact same code smells:

Static code inhibits the following problems:

- Tight coupling, no way to exchange at runtime
- Not mockable
- Static code cannot be overwritten through inheritance
- Global state (increases likelihood of unwanted side effects)

Traits actually have the first three problems themselves and exhibit
the same code smells. But they even have some additional problems on their own:

- Not testable in isolation
- Theoretically stateless, but not enforced in PHP

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

This leads me to the conclusion that traits are just static access in disguise.
Actually you can "rewrite" a PHP 5.4 trait into "pseudo" static code.

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

This actually works right now (and will luckily be removed in PHP 5.5).
Lets reformulate it into something that is actually using static methods:

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

See the familiarity? If Traits can be rewritten as calls to static methods,
how can they be any better than static methods? They exhibit the exact same
problems and produce the same code smells. Traits should be avoided at all
costs, just like static methods.

.. author:: default
.. categories:: PHP
.. tags:: PHP
.. comments::
