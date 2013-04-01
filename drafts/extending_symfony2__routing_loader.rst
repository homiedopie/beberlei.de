Extending Symfony2: Routing Loader
==================================

The Symfony2 routing system is very verbose, requiring routes for every action
in YML, XML or with Annotations (FrameworkExtraBundle). If you are building
an application with a homogeneous routing, you can save considerable effort
mainting all the routes, by implementing your own route loader. Doing
so can free you from copy pasting big chunks of routing information for
new controllers, by automatically building routes based on your own
conventions.

The problem: Repetitive Routing Configuration
---------------------------------------------

For APIs, CRUD applications or other homogenous types of applications
you often have lots of duplication in the routing configuration:

.. code-block:: yaml

    user_list:
        pattern: /user
        defaults: { _controller: AcmeDemoBundle:User:index }
    user_show:
        pattern: /user/{id}/show
        defaults: { _controller: AcmeDemoBundle:User:show }
    user_edit:
        pattern: /user/{id}/edit
        defaults: { _controller: AcmeDemoBundle:User:edit }
    user_remove:
        pattern: /user/{id}/remove
        defaults: { _controller: AcmeDemoBundle:User:remove }

Adding more of entities, you get a multiple of new routes every time.

The solution: A routing loader
------------------------------

If you are following conventions on how how urls map to controller actions
writing your own Routing Loader makes so much sense. Lets invent the following
convention:

- A Controller named ``FooController`` maps to a url ``/foo``
- The ``indexAction`` of your controller maps to the collection root ``/foo``
- Every other action maps to the pattern ``/foo/{id}/{action}`` when the action
  contains a parameter ``$id`` in the signature.
- If no ``$id`` is part of the signature the action maps to ``/foo/{action}``.

We want to register routes for a convention based controller using a very
simple syntax:

.. code-block:: yaml

    user:
        resource: "@AcmeDemoBundle/Controller/UserController.php"
        type: acme_loader

You can implement the routing loader that handles routing resources of the type ``acme_loader``.
We will end up with about 80 lines of routing code, that is completly worth
the effort by forcing us to have routes based on conventions. Required methods
of the ``Loader`` interface are ``supports()`` and ``load()``.

.. code-block:: php

    namespace Acme\DemoBundle\Routing;

    use Symfony\Component\Routing\RouteCollection;
    use Symfony\Component\Routing\Route;
    use Symfony\Component\Config\Resource\FileResource;
    use Symfony\Component\Config\Loader\FileLoader;

    class MyConventionLoader extends FileLoader
    {
        public function supports($resource, $type = null)
        {
            return $type === 'acme_loader';
        }

        public function load($file, $type = null)
        {
            $path = $this->locator->locate($file);

            $class = new \ReflectionClass($this->findClass($path));
            $resourceName = $this->getResourceName($class);

            $collection = new RouteCollection();
            $collection->addResource(new FileResource($path));

            foreach ($class->getMethods() as $method) {
                if (substr($method->getName(), -6) !== "Action") {
                    continue;
                }

                $actionName = $this->getActionName($method);
                $pattern = $this->getActionPattern($actionName, $resourceName, $method);
                $callback = $this->getCallback($class, $method);

                $collection->add(
                    sprintf('%s_%s', $resourceName, $actionName),
                    new Route($pattern, array('_controller' => $callback), array(), array())
                );
            }

            return $collection;
        }

        private function getCallback($class, $method)
        {
            return $class->getName() .'::' . $method->getName();
        }

        private function getActionPattern($actionName, $resourceName, $method)
        {
            if ($actionName == "index") {
                $pattern = sprintf("/%s", $resourceName);
            } else if ($this->containsIdParameter($method)) {
                $pattern = sprintf("/%s/{id}/%s", $resourceName, $actionName);
            } else {
                $pattern = sprintf("/%s/%s", $resourceName, $actionName);
            }

            return $pattern;
        }

        private function getActionName($method)
        {
            return strtolower(str_replace("Action", "", $method->getName()));
        }

        private function getResourceName($class)
        {
            return strtolower(str_replace("Controller", "", $class->getShortname()));
        }

        protected function containsIdParameter($method)
        {
            return array_reduce(function ($contains, $parameter) {
                return $contains || ($parameter->getName() === "id");
            }, $method->getParameters(), false);
        }

        // PSR-0 based class finding using a file name
        protected function findClass($file)
        {
            $pos = strpos($file, "/src") + 5;
            return str_replace( array("/", ".php"), array("\\", ""), substr($file, $pos));
        }
    }

Now enabling this routing loader is simply done by registering the loading
class inside the Dependency Injection Container and tagging it with
``routing.loader``:

    <service id="acme_demo.routing_loader" class="Acme\DemoBundle\Routing\MyConventionLoader">
        <argument type="service" id="file_locator" />
        <tag name="routing.loader" />
    </service>

You can continue adding more conventions to your routing loader such as:

- Auto-detection HTTP Methods (GET, POST, ...) based on method names
- Auto-detection of route attributes based on mehtod arguments
- anything you can come up with...

If you want to implement REST routing, you can take a look at the
`FOSRestBundle <http://github.com/friendsofsymfony/FOSRestBundle>`_ that
implements a routing loader of this kind. The `KnpLabs RADBundle
<http://rad.knplabs.com>`_ implements a CRUD resource based loader.

.. author:: default
.. categories:: none
.. tags:: Symfony
.. comments::
