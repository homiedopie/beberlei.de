Symfony2: A Simple Hello World
==============================

Reading `Simplyfing Django <http://programming.oreilly.com/2014/04/simplifying-django.html>`_
I was reminded of how we organize the `Symfony2 Training at Qafoo <http://qafoo.com/services/training/topics/symfony2.html>`_
to start with a very simple "Hello World" example.

The Symfony2 Standard Edition already contains a huge burden of concepts,
assumptions and conventions that can be confusing for a beginner.

- YAML
- Twig
- Environments and Dependency Injection Container
- Various weird and magic syntaxes for bundles, ``_controller`` and template names
- Various files to open and poke around in
- Composer
- Maybe even Doctrine

As a trainer it is very hard to explain all this at the same time.
It makes a lot of sense to avoid as many of them as possible.

That is why the Standard Edition is not the best way to start teaching Symfony,
but one should actually consider a much lighter version of the framework and
then gradually add more and more features until you end up with the standard
edition.

Fabien discussed the simplification of the Symfony Standard Edition from
another angle before, considering the minimum necessary code to use when
reproducing bugs in his blog post `"Packing a Symfony Full-Stack Application in
one file"
<http://fabien.potencier.org/article/70/packing-a-symfony-full-stack-framework-application-in-one-file-bootstrapping>`_.

This blog post is about a truely minimal Symfony edition to start learning
about the framework.  The first thing I like to show is a really simple Hello
World controller:

.. code-block:: php

    <?php

    namespace Acme\TrainingBundle\Controller;

    use Symfony\Component\HttpFoundation\Response;

    class HelloController
    {
        public function helloAction()
        {
            return new Response('Hello World!');
        }
    }

What is the necessary framework glue code to support this Hello World? Lets start
from the index file `web/index.php`:

.. code-block:: php

    <?php

    require_once __DIR__ . "/../vendor/autoload.php";
    require_once __DIR__ . "/../app/AppKernel.php";

    use Symfony\Component\HttpFoundation\Request;

    $request = Request::createFromGlobals();
    $kernel = new AppKernel('dev', true);
    $kernel->handle($request)->send();

We are using Composer here and the ``AppKernel`` class, lets take a peak
at them:

.. code-block:: php

    {
        "require": {
            "symfony/symfony": "@stable"
        },
        "autoload": {
            "psr-0": { "Acme": "src/" }
        }
    }

The `composer.json` file installs the latest stable Symfony release and
adds autoloading for classes starting with ``Acme`` in the folder `src`.

We need to define a Kernel for our application in `app/AppKernel.php`
and the minimal version of this looks like:

.. code-block:: php

    <?php

    use Symfony\Component\HttpKernel\Kernel;
    use Symfony\Component\Config\Loader\LoaderInterface;

    class AppKernel extends Kernel
    {
        public function registerBundles()
        {
            return array(
                new Symfony\Bundle\FrameworkBundle\FrameworkBundle(),
                new Symfony\Bundle\TwigBundle\TwigBundle(),
            );
        }

        public function registerContainerConfiguration(LoaderInterface $loader)
        {
            $loader->load(function ($container) {
                $container->loadFromExtension('framework', array(
                    'secret' => 'some secret here',
                    'router' => array(
                        'resource' => '%kernel.root_dir%/config/routing.yml'
                    ),
                    'templating' => array('engines' => array('twig'))
                ));
            });
        }
    }

In trainings we are starting with a single ``config.yml`` file but that is
technically not necessary by using the ``ClosureLoader``. The routing
component has no such closure loader, so its not possible to avoid
YAML in the first minutes of Symfony2 exposure and we reference
the `app/config/routing.yml`:

.. code-block:: yaml

    hello:
      pattern: /
      defaults:
        _controller: "Acme\TrainingBundle\Controller\HelloController::helloAction"

Did you know that you can specify controllers in Symfony by using the static callback
syntax? It has disadvantages when considering bundle inheritance, but why
bother a beginner with this feature and confuse him with the convention of
``"AcmeTrainingBundle:Hello:hello"``.

There are still lots of trip wires to stumble upon in this simple piece of ``routing.yml``:

- Tabs are not allowed in YAML, in every training at least one person gets
  bitten by that.
- 2 vs 4 spaces ambiguity.
- What is this magic ``_controller`` key?
- I carefully avoid the ``{}`` inline syntax of YAML here as well as it
  introduces yet another ambiguity.

Run this application with the build in webserver:

::

    $ php -S localhost:8000 web/index.php

Hello World!

The next step for a beginner is his first twig template to print the Hello
World. To avoid another confusing convention at the beginning, the ``"AcmeTrainingBundle:Hello:hello.html.twig"``
template syntax, you can make use of the `app/Resources/views/` folder
that is automatically registered in the Twig Bundle. Just create
a template `app/Resources/views/hello.html.twig` and change the controller:

.. code-block:: php

    <?php

    namespace Acme\TrainingBundle\Controller;

    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Bundle\FrameworkBundle\Controller\Controller;

    class HelloController extends Controller
    {
        public function helloAction()
        {
            return $this->render('hello.html.twig');
        }
    }

The total number of files is 5 (6 with template) for this example. Note that we
haven't actually created a bundle for ``AcmeWorkshopBundle`` yet, because with
the static syntax we don't need it.

This is a very good starting point to start exploring more features of Symfony
and gradually add the required configuration and files for this.
