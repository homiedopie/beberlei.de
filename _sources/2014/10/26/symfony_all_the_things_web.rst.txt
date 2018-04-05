Symfony All The Things (Web)
============================

My `Symfony Hello World post
<http://www.whitewashing.de/2014/04/24/symfony_hello_world.html>`_ introduced
the smallest possible example of a Symfony application. Using this in trainings
helps the participants understand of just how few parts a Symfony application
contains. Sure, there are lots of classes participating under the hood, but
I don't care about the internals only about the public API.

We use microservice architectures for the bepado and `PHP Profiler
<https://tideways.io>`_ projects that Qafoo is working on at the moment. For
the different components a mix of Symfony Framework, Silex, Symfony Components
and our own Rest-Microframework (RMF) are used. This zoo of
different solutions sparked a recent discussion with `my colleague Manuel
<https://twitter.com/manuelp>`_ about when we would want to use Symfony for a
web application.

We quickly agreed on: Always. I can't speak for Manuel, but these are my
reasons for this decision:

- I always want to use a technology that is based on Symfony HttpKernel,
  because of the built-in caching, ESI and the `Stack-PHP
  <http://stackphp.com/>`_ project. I usually don't need this at the beginning
  of a project, but at some point the simplicity of extending the Kernel
  through aggregation is incredible.

  This leaves three solutions: Silex, Symfony Framework and Plain Components.

- I want a well documented and standardized solution. We are working with
  a big team on bepado, often rotating team members for just some weeks or months.

  We can count the hours lost for developers when they have to start learning a
  new stack again. Knowing where to put routes, controllers, templates,
  configuration et al is important to make time for the real tasks.

  This leaves Symfony Framework and Silex. Everything built with the components
  is always custom and therefore not documented well enough.

- I want a stable and extendable solution. Even when you just use Symfony
  for a very small component you typically need to interface with the outside
  world: OAuth, REST-API, HTTP Clients, Databases (SQL and NoSQL). `There is
  (always) a bundle for that
  <http://friendsofsymfony.github.io/slides/there_is_a_bundle_for_that.html#1>`_ in Symfony.

  Yes, Silex typically has a copy-cat Provider for their own DIC system, but
  it is usually missing some configuration option or advanced use-case. In some
  cases its just missing something as simple as a WebDebug Toolbar integration
  that the Symfony Bundle has.

  My experience with Silex has been that its always several steps behind
  Symfony in terms of reusable functionality. One other downside with Silex in
  my opinion is its missing support for DIC and Route caching. Once your Silex
  application grows beyond its initial scope it starts to slow down.

- I want just one solution if its flexible enough.

  It is great to have so many options, but that is also a curse. `Lukas
  <https://twitter.com/lsmith/status/526284891718443009>`_ points out he is picking
  between Laravel, Silex or Symfony depending on the application use-case.

  But the web technology stack is already complex enough in my opionion. I
  rather have my developers learn and use different storage/queue or frontend
  technologies than have them juggle between three frameworks. If my experience
  with Symfony in the last 4 years taught me anything: Hands-on exposure
  with a single framework for that long leads to impressive productivity.

  And Symfony is flexible. The Dependency Injection based approach combined
  with the very balanced decoupling through bundles allows you to cherry-pick
  only what you need for every application: APIs, RAD, Large Teams. Everything
  is possible.

The analysis is obviously biased because of my previous exposure to the
framework. The productivity gains are possible with any framework as long as it
has a flourishing ecosystem. For anyone else this reasoning can end up to
choose Laravel, Silex or Zend Framework 2.

So what is the minimal Symfony distribution that would be a starting point.
Extending on the `Symfony Hello World post <http://www.whitewashing.de/2014/04/24/symfony_hello_world.html>`_:

1. composer.json
2. index.php file
3. A minimal ``AppKernel``
4. A minimal config.yml file
5. routing files
6. A console script
7. A minimal application bundle

You can find `all the code on Github
<https://github.com/beberlei/symfony-minimal-distribution>`_.

Start with the composer.json:

::

    {
        "require": {
            "symfony/symfony": "@stable",
            "symfony/monolog-bundle": "@stable",
            "vlucas/phpdotenv": "@stable"
        },
        "autoload": {
            "psr-0": { "Acme": "src/" }
        }
    }

The index.php:

.. code-block:: php

    <?php
    // web/index.php

    require_once __DIR__ . "/../vendor/autoload.php";
    require_once __DIR__ . "/../app/AppKernel.php";

    use Symfony\Component\HttpFoundation\Request;

    Dotenv::load(__DIR__ . '/../');

    $request = Request::createFromGlobals();
    $kernel = new AppKernel($_SERVER['SYMFONY_ENV'], (bool)$_SERVER['SYMFONY_DEBUG']);
    $response = $kernel->handle($request);
    $response->send();
    $kernel->terminate($request, $response);

We are using the package `vlucas/phpdotenv
<https://github.com/vlucas/phpdotenv>`_ to add `Twelve Factor app
<http://12factor.net/>`_ compatibility, simplyfing configuration. This allows us to get rid of
the different front controller files based on environment. We need a file
called ``.env`` in our application root containing key-value pairs of
environment variables:

::

    # .env
    SYMFONY_ENV=dev
    SYMFONY_DEBUG=1

Add this file to ``.gitignore``. Your deployment to production needs
a mechanism to generate this file with production configuration.

Our minimal AppKernel looks like this:

.. code-block:: php

    <?php
    // app/AppKernel.php

    use Symfony\Component\HttpKernel\Kernel;
    use Symfony\Component\Config\Loader\LoaderInterface;

    class AppKernel extends Kernel
    {
        public function registerBundles()
        {
            $bundles = array(
                new Symfony\Bundle\FrameworkBundle\FrameworkBundle(),
                new Symfony\Bundle\TwigBundle\TwigBundle(),
                new Symfony\Bundle\MonologBundle\MonologBundle(),
                new Acme\HelloBundle\AcmeHelloBundle()
            );

            if (in_array($this->getEnvironment(), array('dev', 'test'))) {
                $bundles[] = new Symfony\Bundle\WebProfilerBundle\WebProfilerBundle();
            }

            return $bundles;
        }

        public function registerContainerConfiguration(LoaderInterface $loader)
        {
            $loader->load(__DIR__ . '/config/config.yml');

            if (in_array($this->getEnvironment(), array('dev', 'test'))) {
                $loader->load(function ($container) {
                    $container->loadFromExtension('web_profiler', array(
                        'toolbar' => true,
                    ));
                });
            }
        }
    }

It points to a configuration file ``config.yml``. We don't use
different configuration files per environment here because we don't
need it. Instead we use the closure loader to enable the web debug
toolbar when we are in development environment.

Symfony configuration becomes much simpler if we don't use the inheritance
and load everything from just a single file:

::

    # app/config/config.yml
    framework:
        secret: %secret%
        router:
            resource: "%kernel.root_dir%/config/routing_%kernel.environment%.yml"
            strict_requirements: %kernel.debug%
        templating:
            engines: ['twig']
        profiler:
            enabled: %kernel.debug%

    monolog:
        handlers:
            main:
                type:         fingers_crossed
                action_level: %monolog_action_level%
                handler:      nested
            nested:
                type:  stream
                path:  "%kernel.logs_dir%/%kernel.environment%.log"
                level: debug

We can set the parameter values for ``%secret%`` and ``%monolog_action_level%``
by adding new lines to ``.env`` file, making use of the excellent `external
configuration parameter support
<http://symfony.com/doc/current/cookbook/configuration/external_parameters.html>`_
in Symfony.

::

    # .env
    SYMFONY_ENV=dev
    SYMFONY_DEBUG=1
    SYMFONY__SECRET=abcdefg
    SYMFONY__MONOLOG_ACTION_LEVEL=debug

Now add a ``routing_prod.yml`` file with a hello world route:

::

    # app/config/routing_prod.yml
    hello_world:
        pattern: /hello/{name}
        defaults:
            _controller: "AcmeHelloBundle:Default:hello"

And because our routes are dependent on the environment in ``config.yml`` also a
``routing_dev.yml`` containing the WebDebug toolbar and profiler routes:

::

    # app/config/routing_dev.yml
    _wdt:
        resource: "@WebProfilerBundle/Resources/config/routing/wdt.xml"
        prefix:   /_wdt

    _profiler:
        resource: "@WebProfilerBundle/Resources/config/routing/profiler.xml"
        prefix:   /_profiler

    _main:
        resource: routing_prod.yml

We now need a bundle ``AcmeHelloBundle`` that is referenced
in routing.yml and in the AppKernel. When we follow Fabiens best practice
about adding services, routes and templates into the ``app/config`` and
``app/Resources/views`` folders adding a bundle just requires the bundle class:

.. code-block:: php

    <?php
    // src/Acme/HelloBundle/AcmeHelloBundle.php

    namespace Acme\HelloBundle;

    use Symfony\Component\HttpKernel\Bundle\Bundle;

    class AcmeHelloBundle extends Bundle
    {
    }

And the controller that renders our Hello World:

.. code-block:: php

    <?php
    // src/Acme/HelloBundle/Controller/DefaultController.php

    namespace Acme\HelloBundle\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\Controller;

    class DefaultController extends Controller
    {
        public function helloAction($name)
        {
            return $this->render(
                'AcmeHelloBundle:Default:hello.html.twig',
                array('name' => $name)
            );
        }
    }

Now we only put a template into ``app/Resources``:

.. code-block:: jinja

    {# app/Resources/AcmeHelloBundle/views/Default/hello.html.twig #}
    Hello {{ name }}!

As a last requirement we need a console script to manage our Symfony
application. We reuse the vlucas/phpdotenv integration here to
load all the required environment variables:

.. code-block:: php

    #!/usr/bin/env php
    <?php
    // app/console

    set_time_limit(0);

    require_once __DIR__.'/../vendor/autoload.php';
    require_once __DIR__.'/AppKernel.php';

    use Symfony\Bundle\FrameworkBundle\Console\Application;
    use Symfony\Component\Console\Input\ArgvInput;

    Dotenv::load(__DIR__ . '/../');

    $input = new ArgvInput();
    $kernel = new AppKernel($_SERVER['SYMFONY_ENV'], (bool)$_SERVER['SYMFONY_DEBUG']);
    $application = new Application($kernel);
    $application->run($input);

Voila. The minimal Symfony distribution is done.

Start the php built in webserver to take a look

::

    $ php -S localhost:8080 web/index.php

I personally like this simplicity of that, the only thing that annoys me are
the two routing files that I need to conditionally load the web profiler routes
and the closure loader for the web_profiler extension. I suppose the nicer
approach would be a compiler pass that does all the magic behind the scenes.

From this minimal distribution you can:

1. Add new services to ``app/config/config.yml``.
2. Add new routes to ``app/config/routing_prod.yml``.
3. Add controllers into new bundles and templates into ``app/Resources``.
4. Add third party bundles or Stack-PHP implementations when you need existing, reusable functionality such
   as OAuth, Databases etc.
5. Add configuration variables to ``.env`` file instead of using the
   ``app/config/parameters.yml`` approach.

This scales well, because at every point you can move towards abstracting
bundles and configuration more using Symfony's built in functionality.
No matter what type of application you build, it is always based on Symfony
and the building blocks are always the same.

I suggest to combine this minimal Symfony with the `QafooLabsFrameworkExtraBundle
<https://github.com/QafooLabs/QafooLabsNoFrameworkBundle>`_ that I `blogged
about two weeks ago
<http://www.whitewashing.de/2014/10/14/lightweight_symfony2_controllers.html>`_.
Not only will the Symfony be lightweight also your controllers. You can built
anything on top this foundation from simple CRUD, APIs, hexagonal- or CQRS-architextures.

.. author:: default
.. categories:: none
.. tags:: Symfony
.. comments::
