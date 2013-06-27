Extending Symfony2: Controller Utilities
========================================

Controllers as a service are a heated topic in the Symfony world. Developers
mainly choose to extend the base class, because its much simpler to use and
less to write. But less to write is not necessarily true.

The problem: Injecting tons of services
---------------------------------------

The Symfony controller base class uses quite a lot of services, if
you need them in your controller as a service, you have to inject them:

.. code-block:: php

    <?php
    class UserController
    {
        public function _construct(
            RouterInterface $router,
            EngineInterface $engine,
            HttpKernel $kernel,
            FormFactoryInterface $formFactory,
            SecurityContextInterface $security
        )
        {
            $this->router = $router;
            $this->engine = $engine;
            $this->kernel = $kernel;
            $this->formFactory = $formFactory;
            $this->security = $security;
        }
    }

There are some problems here:

- The services are not loaded lazily, we probably end up with a resource overuse here.
- The constructor is MUCH too big, this doesn't even include your own
  application, database or mailer services.

The quick and dirty solution
----------------------------

You could as a first solution, inject the container into your controller.
But this is actually the same as just using the base controller from Symfony
or just use the ``ContainerAware`` interface in a controller of your own.

The solution: Introduce a Utilities Service
-------------------------------------------

To avoid the mentioned problems with controller as a service, introduce a
controller utilities service and register it as ``controller_utils`` service:

.. code-block:: php

    <?php

    class ControllerUtils
    {
        private $container;

        public function __construct($container)
        {
            $this->container = $container;
        }

        public function createForm($type, $data, $options)
        {
            // ..
        }

        public function render($template, $parameters)
        {
            // ..
        }
        // ...
    }

You can implement this by just copying the over from
``Symfony\Bundle\FrameworkBundle\Controller\Controller`` all the methods you
need.

Then you can simplify the controller as a service:

.. code-block:: php

    class UserController
    {
        private $utils;

        public function _construct(ControllerUtils $utils)
        {
            $this->utils = $utils;
        }
    }

You don't have to stop here. You can introduce lots of helper objects
and inject them into your controller, depending on your use-cases.
Generic handling of file uploads comes to mind for example.

From medium to large applications this can lead to much smaller
controllers, because they can much more easily reuse code between
each other than in the case of inheritance.

.. author:: default
.. categories:: none
.. tags:: Symfony
.. comments::
