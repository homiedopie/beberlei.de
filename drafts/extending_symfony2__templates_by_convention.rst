Extending Symfony2: Templates by Convention
===========================================

In a Symfony2 application you are usally rendering templates
for controllers explicitly. Based on usual Framework conventions
however, the template names could easily be automatically
detected based on Controller + Action name.

The problem: Rendering Templates by name epxlicitly
---------------------------------------------------

Rendering templates by name is verbose, like the following example shows:

.. code-block:: php

    <?php
    class UserController extends Controller
    {
        public function showAction(User $user)
        {
            return $this->render('AcmeDemoBundle:User:show.html.twig', array(
                'user' => $user
            ));
        }
    }

We want to avoid calling ``$this->render`` and return an array of data only.
The template name should be automatically inferred from the controller + action.

The quick and dirty solution
----------------------------

Inheritance provides the quick and dirty solution, adding a simple helper
method to our base controller. It doesn't free us from calling a function
in the action, but it saves us from typing the template name:

.. code-block:: php

    <?php
    abstract class BaseController extends Controller
    {
        public function quickRender(array $data)
        {
            list($controller, $action) = explode("::", $this->getRequest()->attributes->get('_controller'));
            $bundle = $this->getBundle($controller);
            $controller = $this->getControllerShortName($controller);

            return $this->render(sprintf('%s.%s.%s.twig.html',
                $bundle, $controller, $action), $data);
        }

        private function getControllerShortName($className)
        {
            $refl = new \ReflectionClass($className);
            return str_replace("Controller", "", $refl->getShortname());
        }

        private function getBundle($className)
        {
            $kernel = $this->container->get('kernel');

            foreach ($kernel->getBundles() as $bundle) {
                if (strpos($className, $bundle->getNamespace())) {
                    return $bundle->getName();
                }
            }

            throw new \RuntimeException("Class $className is not in a bundle.");
        }
    }

We can just call ``$this->quickRender(array('user' => $user));`` with this
helper method now.

The solution: A kernel.view Event Listener
------------------------------------------

A cleaner solution allows us to return an array only, and doing all the
template resolving magic automatically during the ``kernel.view`` event.

SensioFrameworkExtraBundle does this out of the box with the ``@Template``
annotation, however we wan't to do better and skip even this annotation all
together.

The first step is extracting the code for bundle and controller name
detection into a service class, we call it ``SymfonyClassUtils``.
We can actually use these methods in other contexts as well and I will
refer back to them in future blog posts of this series:

.. code-block:: php

    <?php
    class SymfonyClassUtils
    {
        private $kernel;

        public function __construct($kernel)
        {
            $this->kernel = $kernel;
        }

        public function getControllerShortName($className)
        {
            $refl = new \ReflectionClass($className);
            return str_replace("Controller", "", $refl->getShortname());
        }

        public function getBundleForClass($className)
        {
            foreach ($this->kernel->getBundles() as $bundle) {
                if (strpos($className, $bundle->getNamespace())) {
                    return $bundle->getName();
                }
            }

            throw new \RuntimeException("Class $className is not in a bundle.");
        }
    }

Now the ``kernel.view`` helper is just a simple listener that checks if a
controller returned an array only, and if so uses the class utils.

.. code-block:: php

    <?php

    use Symfony\Component\HttpKernel\Event\GetResponseForControllerResultEvent;

    class TemplateDetectionListener
    {
        private $container;
        private $classUtils;

        public function __construct($container, $classUtils)
        {
            $this->container = $container;
            $this->classUtils = $classUtils;
        }

        public function onKernelView(GetResponseForControllerResultEvent $event)
        {
            $parameters = $event->getControllerResult();

            if (!is_array($parameters)) {
                return;
            }

            $templating = $this->container->get('templating');
            list($controller, $action) = $event->getRequest()->attributes->get('_controller');

            $bundle = $this->classUtils->getBundle($controller);
            $controller = $this->classUtils->getControllerShortName($controller);
            $template = sprintf('%s.%s.%s.twig.html', $bundle, $controller, $action);

            $event->setResponse($templating->renderResponse($template, $parameters));
        }
    }

Register this listener with the Dependency Injection Container and you are good
to go:

.. code-block:: xml

    <service id="acme_demo.template_detection_listener"
             class="Acme\DemoBundle\Listener\TemplateDetectionListener">
        <argument type="service" id="service_container" />
        <argument type="service" id="acme_demo.class_utils" />

        <tag name="kernel.event_subscriber" event="kernel.view" />
    </service>

Rendering templates now simplifies to:

.. code-block:: php

    <?php
    class UserController extends Controller
    {
        public function showAction(User $user)
        {
            return array('user' => $user);
        }
    }

.. author:: default
.. categories:: none
.. tags:: Symfony
.. comments::
