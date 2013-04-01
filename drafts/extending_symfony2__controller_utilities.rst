Extending Symfony2: Controller Utilities
========================================

Controllers as a service a heated topic in the Symfony world. Developers
mainly choose to extend the base class, because its much simpler to use and
less to write. But this doesn't have to be the case.

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

The solution: Introduce a Utilities Service
-------------------------------------------

To avoid the mentioned problems with controller as a service, introduce a
controller utilities service:

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

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
