:author: beberlei <kontakt@beberlei.de>
:date: 2008-09-20

Dependency Injection via Interface in PHP: An example
=====================================================

Personal projects and work currently both force me to think about
application design and I `came accross dependency
injection <http://www.martinfowler.com/articles/injection.html>`_ the
other day. Its quite a complex Design Pattern and hard to grasp, even
with the number of examples you can find in the internet. Basically
Dependency Injection means you register components that might be a
dependency for other components and when loading new classes via the
dependency injection framework, it knows of this relationsships and
assembles the object in need and all its dependencies and returns them
fully initialized. This pattern leads to completly encapsulated objects
where any class in the object graph can be exchanged for a new
implementation without breaking all its dependencies. It also makes
testing complex components and object relationsships very easy.

Asfar as I could find out, three different types of Dependency Injection
implementations exist: Via Constructor, via Setter and via Interfaces.
There exist implementations of Dependency Injection for Java (Spring)
that are configured via XML config files and seem very complex. They are
also hard to read in code I pressume, since you always have to be aware
of the current application configuration. There are also some more
lightweight implementations (PicoContainer) that assemble their
relationsships in the application and work with config methods that act
as configuration of the dependancies. `Martin Folwer also discusses an
implementation via
interfaces <http://www.martinfowler.com/articles/injection.html>`_,
which seems most accessible for me.

All PHP clones of any dependancy injection framework seem to go the
complex way via configuration though. With traits and multiple class
inheritance on the horizon, some kind of interface injection seems
mighty powerful though. So I implemented a really lightweight
implementation of Interface Dependency Injection for PHP. The Container
works with static method only, is therefore in the global scope, such
that configuration is reduced to a minimum. Generally you have to write
interfaces for object injection, for example:

    ::

        interface InjectDbAdapter{  public function injectDbAdapter(Zend_Db_Adapter_Abstract $db);}

Other potential examples include "InjectLogger", "InjectSoapClient", or
"InjectAppConfig". You then have to register a component for usage with
this interface:

    ::

        Whitewashing_Container::registerComponent('InjectDbAdapter', Zend_Db::factory($dbConfig));

Now any class that implements the InjectDbAdapter interface can be
instantiated via:
    ::

        $obj = Whitewashing_Container::load('Class');

and the loader takes care of calling the 'Class' implementation of
injectDbAdapter with the given Database Adapter. A negative consequence
of this approach is that you have to implement the inject methods for
all interfaces in your concrete class implementations. With Traits
(multiple class inheritence) being a new feature in PHP soon, injection
via parent classes seems to become a very powerful approach though,
which can handle the concrete implementations.

The Container takes care of all the dependancy building, so when testing
your components you can register lots of mock objects. You can also
exchange dependancies for only a subset of objects very easily. I
implemented a method "Whitewashing\_Container::registerClassComponent",
which registers a dependency component that is used with higher priority
in construction of the given class. You can also specify a third
parameter $localInterfaceOverride for the highest priority:

    ::

        $obj = Whitewashing_Container::load('Class', null, array('InjectDbAdapter' => $newDbAdapter));

Speedwise the usage of the Container reduces class instatiation by about
50%, from 0.5 sec for 10000 classes with setting dependencies to 1 sec
on my machine. But naturally only classes with dependancies and lots of
them should be using this mechanism and with good application design,
this shouldn't be to many. You can download
`Container <http://www.beberlei.de/sources/WhitewashingContainer.phps>`_
and `Example <http://www.beberlei.de/sources/di.phps>`_ sourcecode, to
take a look. Currently this Container is not really creating new
dependencies for each new class generation but rather inverts the usage
of a registry. It should be an easy task to extend the registering
method to decide between new class generation and using the globally
registered class instance.
