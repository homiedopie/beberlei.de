Dependecy Injection the juicy way
=================================

I have written on dependency injection before and `came up with a
solution for PHP via interface
injection <http://www.whitewashing.de/blog/articles/83>`_. Thinking
about it twice I didn't like it very much. Its too much overkill that
you have to implement all setter methods again and again.

Still dependency injection is the way to write good, testable and easily
exchanged and re-wired object graphs. I tried to do lots of dependency
injection via constructor lately and realized that it polutes my
constructors when my object graph is too deep.

An example: When I setup my database connection in the bootstrap file
and encapsulate it in my model creation factory object, i have to insert
the model factory through the configuration into the dispatcher into the
different controllers and views to be accessible in the MVC pattern. The
model factory has to walk 3 nodes in the object graph without being used
at all in the "higher" steps. This creates very unnecessary
dependencies.

I came across `Misko Hevery <http://misko.hevery.com/>`_'s Blog, which
rocks. There are also some `great Google Tech Talks by
him <http://www.youtube.com/results?search_query=misko+hevery&search_type=&aq=f>`_,
where he argues in favour of dependency injection and debunks singletons
as being evil (he does that on his blog too). From there I learnt about
`Guice <http://code.google.com/p/google-guice/>`_, a dependency
injection framework for Java by Google.

What I like about Guice: Its easy to use and its immediatly obvious to
someone without experience, why it works so good and you don't have to
hand down objects deep down the object graph. I cloned the basic
functionality for PHP and an example would work as follows.

We first have to implement a **module**, which defines which concrete
implementation should be injected as a placeholder for which interface.

    ::

        class ServiceModule implements Module{ public function configure(Binder $b) {  $b->bind("Service")->to("ConcreteService");  $b->bind("Add")->to("ConcreteAdd");  $b->bind("Sub")->to("ConcreteSub"); }}

We can now use this module to instantiate an injector object:

    ::

        $injector = new Injector( new ServiceModule() );$service = $injector->getInstance("Service");

Given that the constructor of **ConcreteService** would expect an Add
and a Sub object, the Injector would realize this and instantiate the
concrete implementations **ConcreteAdd** and **ConcreteSub** and inject
them into the constructor.

What makes this dependency injection so simple and great to use? You can
instantiate an injector everywhere in your code and just have to
configure it using the additional module implementation. This way you
don't have to make sure that you pass down the dependency injection
container from the bootstrap into all nodes of the application. You can
also easily work with many frameworks and still be able to use
dependency injection without having to hack the whole core of the
framework.

My guice clone does more. It allows to pass down additional non-object
arguments into constructors, even for object dependencies. It offers a
**Provider** interface to be able to wrap adapters around your already
existing ServiceLocator or Registry objects. But its reflection
capabilities have to be extended to docblock comments, so that better
dependency detection is possible.

Because using dependency injection with only this little example I will
refrain from releasing the source code yet. I have to provide some
useful documentation for it to be of use to anyone.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>