PHPunit @before Annotations and traits for code-reuse
=====================================================

I have written about why I think `traits should be avoided
<http://www.whitewashing.de/2013/04/12/traits_are_static_access.html>`_. There
is a practical use-case that serves me well however: Extending PHPUnit tests.

The PHPUnit TestCase is not very extendable except through inheritance. This
often leads to a weird, deep inheritance hierachy in testsuites to achieve code
reuse. For example the Doctrine ORM testsuite having ``OrmFunctionalTestCase``
extending from ``OrmTestCase`` extending from PHPUnits testcase.

Dependency Injection is something that is not possible easily in a PHPUnit
testcase, but could be solved using an additional listener and some
configuration in ``phpunit.xml``.

This leaves traits as a simple mechanism that doesn't require writing an
extension for PHPUnit and allows "multiple inheritance" to compose different
features for our test cases.

See this simple example that is adding some more assertions:

.. code-block:: php

    <?php

    trait MyAssertions
    {
        public function assertIsNotANumber($value)
        {
            $this->assertTrue(is_nan($value));
        }
    }

    class MathTest extends \PHPUnit_Framework_TestCase
    {
        use MyAssertions;

        public function testIsNotANumber()
        {
            $this->assertIsNotANumber(acos(8));
        }
    }

When you have more complex requirements, you might need the trait to implement
``setUp()`` method. This will prevent you from using multiple traits that all
need to invoke ``setUp()``. You could use the trait conflict resolution, but
then the renamed setup methods do not get called anymore.

Fortunately PHPUnit 3.8+ comes to the rescue with new ``@before`` and
``@beforeClass`` annotations.

See this trait I use for making sure my database is using the
most current database version by invoking migrations in ``@beforeClass``

.. code-block:: php

    <?php

    namespace Xhprof;

    use Doctrine\DBAL\DriverManager;

    trait DatabaseSetup
    {
        /**
         * @var bool
         */
        private static $initialized = false;

        /**
         * @beforeClass
         */
        public static function initializeDatabase()
        {
            if (self::$initialized) {
                return;
            }

            self::$initialized = true;

            $conn = DriverManager::getConnection(array(
                'url' => $_SERVER['TEST_DATABASE_DSN']
            ));

            $dbDeploy = new DbDeploy($conn, realpath(__DIR__ . '/../../src/schema'));
            $dbDeploy->migrate();
            $conn->close();
        }
    }

I could mix this with a second trait ``SymfonySetup`` that makes the DIC
container available for my integration tests:

.. code-block:: php

    <?php

    namespace Xhprof;

    trait SymfonySetup
    {
        protected $kernel;
        protected $container;

        /**
         * @before
         */
        protected function setupKernel()
        {
            $this->kernel = $this->createKernel();
            $this->kernel->boot();

            $this->container = $this->kernel->getContainer();
        }

        protected function createKernel(array $options = array())
        {
            return new \AppKernel('test', true);
        }

        /**
         * @after
         */
        protected function tearDownSymfonyKernel()
        {
            if (null !== $this->kernel) {
                $this->kernel->shutdown();
            }
        }
    }

The Symfony setup trait uses ``@before`` and ``@after`` to setup and cleanup
without clashing with the traditional PHPUnit ``setUp`` method.

Combining all this we could write a testcase like this:

.. code-block:: php

    <?php

    class UserRepositoryTest extends \PHPUnit_Framework_TestCase
    {
        use DatabaseSetup;
        use SymfonySetup;

        public function setUp()
        {
            // do setup here
        }

        public function testNotFindUserReturnsNull()
        {
            $userRepository = $this->container->get('user_repository');
            $unusedId = 9999;
            $user = $userRepository->find($unusedId);
            $this->assertNull($user);
        }
    }

Sadly the ``@before`` calls are invoced *after* the original ``setup()`` method
so we cannot access the Symfony container here already. Maybe it would be more
practical to have it work the other way around. I have `opened an issue on
PHPUnit <https://github.com/sebastianbergmann/phpunit/issues/1616>`_ for that.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
