.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Using Symfony Dependency Injection with Zend_Application
========================================================

As a follow-up to my `recent
post <http://www.whitewashing.de/blog/articles/117>`_ on Dependency
Injection containers and Zend\_Application I was eager to find out if
its possible to integrate the new `Symfony Dependency Injection
Container <http://components.symfony-project.org/dependency-injection/>`_
into the Zend Framework. To my suprise its possible without having to
make any changes to one of the two components. An example use-case would
look like:

    ::

        $container = new sfServiceContainerBuilder();
         
        $loader = new sfServiceContainerLoaderFileXml($container);
        $loader->load(APPLICATION_PATH.'/config/objects.xml');

        $application = new Zend_Application(
            APPLICATION_ENV,
            APPLICATION_PATH . '/config/application.xml'
        );
        $application->getBootstrap()->setContainer($container);
        $application->bootstrap()
                    ->run();

Resources instantiated by Zend\_Application are then injected into the
container by the name of the resource and are given the resource
instance. Any object from the Symfony container can then use these
dependencies in their object setup. The only drawback of the integration
is the fact that the Symfony Container is case-sensitive in regards to
the service names but Zend\_Application lower-cases all service before
injecting them into the container. The following code is a restatement
of my previous example of a **MyModel** class which requires a
**Zend\_Db** and **Zend\_Cache** constructor argument.

    ::

        $container->register('myModel', 'MyModel')
                  ->addArgument(new sfServiceReference('db'))
                  ->addArgument(new sfServiceReference('cache'));

Access to a MyModel instance with its dependencies is then granted
through the call **$container->myModel** throughout the application.
Make sure to call this after running Zend\_Application::bootstrap, so
that the Resource dependencies are injected first.
