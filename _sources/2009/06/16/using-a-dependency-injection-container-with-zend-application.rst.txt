Using a Dependency Injection Container with Zend_Application
============================================================

Much has been written on Dependency Injection lately, mostly by Padraic
Brady
(`1 <http://blog.astrumfutura.com/archives/394-The-Case-For-Dependency-Injection-Part-1.html>`_,
`2 <http://blog.astrumfutura.com/archives/395-The-Case-For-Dependency-Injection-Part-2.html>`_)
and Fabien Potencier
(`1 <http://fabien.potencier.org/article/11/what-is-dependency-injection>`_,
`2 <http://fabien.potencier.org/article/12/do-you-need-a-dependency-injection-container>`_,
`3 <http://fabien.potencier.org/article/13/introduction-to-the-symfony-service-container>`_,
`4 <http://fabien.potencier.org/article/14/symfony-service-container-using-a-builder-to-create-services>`_,
`5 <http://github.com/fabpot/Pimple/tree/master>`_). My subjective
feeling tells me there are now more PHP DI containers out there than CMS
or ORMs implemented in PHP, including two written by myself (an
`overengineered <http://www.beberlei.de/sphicy/>`_ and `a useful
one <http://github.com/beberlei/yadif/tree/master>`_). Its an awesome
pattern if used on a larger scale and can (re-) wire a complex business
application according to a clients needs without having to change much
of the domain code. It aims at a complete separation of object
instantiation and dependency tracking from the business logic.

Beginning with version 1.8 Zend Framework is able to integrate any of
these DI containers into its **Zend\_Application** component easily. The
Application component initializes a set of common resources and pushes
them into the MVC stack as additional Front Controller parameters.
Technically a **Zend\_Registry** instance holds all these resources with
their respective resource names as keys. The resources are accessible
inside the Front Controller and the Action Controller classes. Assume
the resource 'Db' is initialized in your application, you can access it
with:

    ::

        $front = Zend_Controller_Front::getInstance();
        $container = $front->getParam('bootstrap')->getContainer();
        $db = $container->db;

        // or:
        class FooController extends Zend_Controller_Action {
            public function barAction()
            {
                $container = $this->getInvokeArg('bootstrap')->getContainer();
                $db = $container->db;
            }
        }

This is pretty much dependency injection already, but the default
registry approach suffers from two serious problem: New instances can
only be added to the Container by implementing new Zend\_Application
resources and these instances cannot be lazy loaded. All resources used
by Zend\_Application are always loaded on every request. But the
application container implementation was developed with Dependency
Injection in mind and is not tied to the use of Zend\_Registry. Only
three magic methods are required by any container that wants to be
Zend\_Application compliant: \_\_get(), \_\_set() and \_\_isset(). Each
instantiated resource is pushed via \_\_set() into the container. If
required by another resource, \_\_isset() is used to check whether a
resource with the given name exists inside the container and \_\_get()
is used to retrieve the instances from the container.

Some month ago I extended
`Yadif <http://github.com/beberlei/yadif/tree/master>`_, a lightweight
PicoContainer-like DI container for PHP written by Thomas McKelvey, with
several features that make it a very powerful DI container in my
opinion. It has a detailed documentation and examples on the GitHub Page
if you want to check it out. I extended Yadif to be Zend\_Application
compliant in a way that the application-wide Zend\_Application resources
can be used as dependencies for objects that are lazy-loaded from the
container. Skipping the tech-talk, here is an example. First we have to
replace the default Container with Yadif:

    ::

        $objects = new Zend_Config_Xml(APPLICATION_PATH."/config/objects.xml");
        $container = new Yadif_Container($objects);

        $application = new Zend_Application(
            APPLICATION_ENV,
            APPLICATION_PATH . '/config/application.xml'
        );
        // Set Yadif as Container
        $application->getBootstrap()->setContainer($container);
        $application->bootstrap()
                    ->run();

Assume you run Zend\_Application with a "Db" and a "Cache" resource.
These resources are loaded on every request. The objects configured in
Yadif however are not instantiated until they are requested for the
first time from the container. We can merge these two worlds and make
use of the Application resources inside the Yadif Configuration
"objects.xml", which looks like:

    ::

        <?xml version="1.0" ?>
        <objects>
            <myModel>
                <class>MyModel</class>
                <arguments arg1="db" arg2="cache" />
            </myModel>
        </objects>

    Instantiating a **myModel** class inside the Action Controller uses
    the the Database and Cache resources as constructor arguments:

        ::

            class FooController extends Zend_Controller_Action {
                public function barAction()
                {
                    $container = $this->getInvokeArg('bootstrap')->getContainer();
                    $myModel = $container->myModel;
                }
            }

    Given the possibilites by the Yadif\_Container you are now empowered
    to use Dependency Injection for all your application objects and
    make use of Zend\_Applications resource system. Furthermore any
    other dependency injection container, simple or complex, can also be
    integrated easily.

.. categories:: none
.. tags:: ZendFramework, DependencyInjection, YadifLibrary
.. comments::
