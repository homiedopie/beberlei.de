Dependency Injection with PHP: Introducing Sphicy
=================================================

I have written `on dependency
injection <http://www.whitewashing.de/blog/articles/101>`_ before
christmas and how `Guice <http://code.google.com/p/guice>`_, googles DI
framework, offers a simple solution. I copied the functionality for a
PHP clone of Guice and named it
`Sphicy <http://www.beberlei.de/sphicy>`_. You saw an early prototype of
it in the blogpost mentioned above.

`Sphicy <http://www.beberlei.de/sphicy>`_ configures object dependencies
with modules: You explicitly state which implementation should be bound
to which interface. An injector then creates instances of these objects
via reflection: All constructor dependencies are resolved by looking at
the given type hints and initializes those according to the specified
bindings.

Two examples included in the `source code of
Sphicy <http://www.beberlei.de/dev/svn/sphicy/>`_ are `Zend
Framework <http://framework.zend.com>`_ and
`ezComponents <http://www.ezcomponents.org>`_ MVC bootstrapping modules.
Sadly both frameworks default front controllers are engineered in such a
way that useful dependency injection needs some workarounds.

As an example I will now discuss the Sphicy Module for Zend Framework
MVC applications. To circumvent the singleton and protected Constructor
of Zend\_Controller\_Front, we have to build a new front controller that
wraps around it and requires all the dependencies:

    ::

        class Sphicy_Controller_Front
        {
            protected $front;

            /**
             * Create Front Controller for Zend Framework using explicitly dependencies created by Sphicy.
             *
             * @param Zend_Controller_Request_Abstract      $request
             * @param Zend_Controller_Response_Abstract     $response
             * @param Zend_Controller_Router_Interface      $router
             * @param Zend_Controller_Dispatcher_Interface  $dispatcher
             */
            public function __construct(
                Zend_Controller_Request_Abstract $request,
                Zend_Controller_Response_Abstract $response,
                Zend_Controller_Router_Interface $router,
                Zend_Controller_Dispatcher_Interface $dispatcher=null
            )
            {
                $front = Zend_Controller_Front::getInstance();
                $front->setRequest($request);
                $front->setResponse($response);
                $front->setRouter($router);

                if($dispatcher === null) {
                    $dispatcher = $front->getDispatcher();
                }
                $front->setDispatcher($dispatcher);
            }

            public function dispatch()
            {
                $this->front->dispatch();
            }
        }

You can see that the **Sphicy\_Controller\_Front** class requires
dependencies in its constructor that are then forward injected into
**Zend\_Controller\_Front**. You can now create a module that binds all
the required dependencies to concrete implementations, for example a
module for a Zend MVC Http Application might look like:

    ::

        class Sphicy_ZendMvc_ExampleModule implements spModule {
             public function configure(spBinder $binder) {
                 // Sphicy_Controller_Front does not extend Zend_Controller_Front, because of Singletonitis
                 // It offers the dispatch method to proxy against Zend_Controller_Front::dispatch.
                 $binder->bind("Sphicy_Controller_Front")->to("Sphicy_Controller_Front");
                 $binder->bind("Zend_Controller_Request_Abstract")->to("Zend_Controller_Request_Http");
                 $binder->bind("Zend_Controller_Response_Abstract")->to("Zend_Controller_Response_Http");
                 // loads all routes
                 $binder->bind("Zend_Controller_Router_Interface")->to("MyApplication_Router");
             }
         }

The class **MyApplication\_Router** might look up all the routing
information of the application via a hardcoded configuration mechanism.
You may say this is a hard dependency, but actually you can just switch
modules or implementations at this position to replace the router with
another implementation. You can also see that no implementation for the
dispatcher is bound. But this dependency is optional and will be created
automatically as can be seen in the **Sphicy\_Controller\_Front** class.

The front controllers is now created by calling:

    ::

        $injector = new spDefaultInjector(new Sphicy_ZendMvc_ExampleModule());
        $front = $injector->getInstance("Sphicy_Controller_Front");
        $front->dispatch();

What happens in the **$injector->getInstance()** line? Sphicy looks at
**Sphicy\_Controller\_Front**'s constructor and finds that four
dependencies are needed: Request, Response, Router and Dispatcher
implementations. It looks up the bindings and searches for them,
creating Zend\_Controller\_Request\_Http,
Zend\_Controller\_Response\_Http and MyApplication\_Router objects. A
dispatcher implementation is not found, but Sphicy recognizes that null
is a valid paramater and injects it. The 3 concrete implementations and
one null are instantiated and used to construct a valid
**Sphicy\_Controller\_Front** instance.

You have now stated the dependencies of the Zend Controller Front
explicitly and can switch them instantaneously by switching the bindings
of interface to implementations in the configuration module.

Have a look at the `Sphicy Website <http://www.beberlei.de/sphicy>`_ and
`FAQ <http://www.beberlei.de/sphicy/documentation/faq.html>`_ to see
more examples and information about the possibilites of this dependency
injection framework.

.. categories:: none
.. tags:: DependencyInjection, SphicyLibrary
.. comments::
