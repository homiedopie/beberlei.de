The ContainerTest
=================

This is a short post before the weekend about testing in applications with
dependency injection container (DIC). This solution helps me with a problem
that I occasionally trip over in environments with large amounts of services
connected through a DIC.

The problem is forgetting to adjust the DIC configuration when you add a new or
remove a dependency to a service. This can easily slip through into production
if you rely on your functional- and unit-tests to catch the problem.

I can avoid this problem by adding a functional test in my application that
instantiate all the various services and checks if they are created correctly.
The first time I saw this pattern was during development of some of the early
Symfony2 bundles, most notably DoctrineBundle.

.. code-block:: php

    <?php

    namespace Acme;

    class ContainerTest extends \PHPUnit_Framework_TestCase
    {
        use SymfonySetup;

        public static function dataServices()
        {
            return array(
                array('AcmeDemoBundle.FooService', 'Acme\DemoBundle\Service\FooService'),
                array('AcmeDemoBundle.BarController', 'Acme\DemoBundle\Controller\BarController'),
            );
        }

        /**
         * @test
         * @dataProvider dataServices
         */
        public function it_creates_service($id, $class)
        {
            $service = $this->getContainer()->get($id);
            $this->assertInstanceOf($class, $service);
        }
    }

Whenever you create or modify a service check the ContainerTest if its already
guarded by a test. Add a test if necesary and then make the change. It's as
easy as that.

The ``SymfonySetup`` trait provides access to the Symfony DIC using
``getContainer()`` as you can see in the test method. See `my blog post
<http://www.whitewashing.de/2015/02/14/phpunit_before_annotations_and_traits_for_code_reuse.html>`_
on traits in tests for more information.

.. author:: default
.. categories:: none
.. tags:: Symfony, Testing
.. comments::
