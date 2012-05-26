.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Symfony2 Controller Testing without Application
===============================================

Controller testing using the WebTestCase requires a Symfony Kernel and with
that a complete application. However you can just ship your own simple kernel
with just the dependencies necessary to test your application. This way you can
easily create functional tests for bundles without the bundle requiring an
application.

Create a TestKernel
-------------------

.. code-block:: php

    <?php
    // Tests/Controller/App/AppKernel.php

    use Symfony\Component\HttpKernel\Kernel;
    use Symfony\Component\Config\Loader\LoaderInterface;

    class AppKernel extends Kernel
    {
        public function registerBundles()
        {
            $bundles = array(
                // Dependencies
                new Symfony\Bundle\FrameworkBundle\FrameworkBundle(),
                new Symfony\Bundle\SecurityBundle\SecurityBundle(),
                new Symfony\Bundle\MonologBundle\MonologBundle(),
                new Symfony\Bundle\TwigBundle\TwigBundle(),
                new Sensio\Bundle\FrameworkExtraBundle\SensioFrameworkExtraBundle(),
                new JMS\SerializerBundle\JMSSerializerBundle($this),
                new FOS\RestBundle\FOSRestBundle(),
                // My Bundle to test
                new Beberlei\WorkflowBundle\BeberleiWorkflowBundle(),
            );

            return $bundles;
        }

        public function registerContainerConfiguration(LoaderInterface $loader)
        {
            // We dont need that Environment stuff, just one config
            $loader->load(__DIR__.'/config.yml');
        }
    }

Creating the config.yml
-----------------------

.. code-block:: yml

    # Tests/Controller/App/config.yml
    framework:
        secret:          secret
        charset:         UTF-8
        test: ~
        router:          { resource: "%kernel.root_dir%/routing.yml" }
        form:            true
        csrf_protection: true
        validation:      { enable_annotations: true }
        templating:      { engines: ['twig'] }
        session:
            auto_start:     false
            storage_id: session.storage.filesystem

    monolog:
        handlers:
            main:
                type:         fingers_crossed
                action_level: error
                handler:      nested
            nested:
                type:  stream
                path:  %kernel.logs_dir%/%kernel.environment%.log
                level: debug


Creating the routing.yml
------------------------

.. code-block:: yml

    # Tests/Controller/App/routing.yml
    BeberleiWorkflowBundle:
        resource: "@BeberleiWorkflowBundle/Controller/"
        type:     annotation
        prefix:   /

Adding a PHPUnit bootstrap
--------------------------

I assume the setup that Henrik described in his "`Travis & Composer sitting in a
Tree K-I-S-S-I-N-G" blog post
<http://henrik.bjrnskov.dk/travis-and-composer-sitting-in-a-tree/>`_.

His setup is missing the spl_autoload_register() call in the bootstrap file
though.

.. code-block:: php

    <?php
    // Tests/bootstrap.php
    $loader = @include __DIR__ . '/../vendor/.composer/autoload.php';
    if (!$loader) {
        die(<<<'EOT'
    You must set up the project dependencies, run the following commands:
    wget http://getcomposer.org/composer.phar
    php composer.phar install
    EOT
        );
    }
    \Doctrine\Common\Annotations\AnnotationRegistry::registerLoader(array($loader, 'loadClass'));

    spl_autoload_register(function($class) {
        if (0 === strpos($class, 'Beberlei\\WorkflowBundle\\')) {
            $path = __DIR__.'/../'.implode('/', array_slice(explode('\\', $class), 2)).'.php';
            if (!stream_resolve_include_path($path)) {
                return false;
            }
            require_once $path;
            return true;
        }
    });

That means your bundle should have a composer.json that loads all the
dependencies.

Modifying the phpunit.xml.dist
------------------------------

We have to tell the WebTestCase base class where to find this kernel:

.. code-block:: xml

    <!-- phpunit.xml.dist -->
    <phpunit bootstrap="Tests/bootstrap.php">
        <php>
            <server name="KERNEL_DIR" value="Tests/Controller/App" />
        </php>
    </phpunit>

Now just run your web-test cases.

If you want to debug the logging happing inside the Kernel just comment out
the Monolog lines to get the log-messages printed to the screen.

You have to add the `Tests/App/cache` and `Tests/App/logs` to your version
control ignore files.
