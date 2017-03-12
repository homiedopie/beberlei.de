Explicit Global State with Context Objects
==========================================

Global State is considered bad for maintainability of software. Side effects on
global state can cause a very nasty class of bugs. Context objects are one
flavour of global state. For example, I remember that Symfony1 had a
particularly nasty context object that was a global singleton containing
references to very many services of the framework.

As with every concept in programming, there are no absolute truths though and
there are many use-cases where context objects make sense. This blog posts
tries to explain my reasons for using context objects.

What is a Context?
------------------

Context is defined as all the information and circumstances in which
something can be *fully* understood. In daily programming this is mostly
related to the state of variables and databases. Some examples in the world
of PHP include the superglobals ``$_GET`` and ``$_POST``.

Any piece of code is always running in some context and the question is how much
of it is explicit in the code and how much is hidden.

A context object is a way to make the existing context explicit for your code.

Context Objects
---------------

Lets take a look at the Definition of a context object

    A context object encapsulates the references/pointers to services and
    configuration information used/needed by other objects. It allows the objects
    living within a context to see the outside world. Objects living in a different
    context see a different view of the outside world.

Besides the obvious use of encapsulating services and config variables, this
definition mentions two important properties:

1. Allows to see the outside world, which does *not* mean it can change it.
   In my opinion it is essential that context objects are immutable,
   to avoid side effects.   

2. The possibility of objects living in different contexts, seeing
   different context objects suggets that a context object
   should never be a singleton.

By using objects instead of global variables for context, we can use
encapsulation to achieve immutability.

Context already exists in PHP through the existance of superglobals. Frameworks
usually wrap them to achieve the properties mentioned above: Immutability and
Not-Singleton.

The Symfony Request object is one good example, where these properties (almost)
hold. Wrapping the superglobals with this object even allowed creating
Subrequests inside PHP requests.

Application Context
-------------------

Now that we have defined context we should make use of context objects in your
applications.

Anything that is an important global information in your application is
relevant for the context:

1. Building a wiki? I actually have the idea for this approach from
   `Fitnesse <http://www.fitnesse.org/>`_, a testing tool based on the wiki idea maintained by Uncle Bob
   and his team. Their `context object
   <https://github.com/unclebob/fitnesse/blob/master/src/fitnesse/FitNesseContext.java>`_ provides access to the current and the
   root page nodes.

2. Building a shop? The users basket id, selected language/locale, current
   campaign (newsletter, google, social media?) can be information that should
   be available all the time.

3. Building an analytics software? The currently selected date/time-range is
   probably important for all queries.

4. Building a CMS/blog? The current page/post-id, the root page id, user
   language/locale seem to be good candidates for an application context. 
   Wordpress does this although their context is global and encapsulated in an
   object.

5. Building a multi-tenant app? The tenant-id and configuration for this
   tentant (selected product plan, activated features, ...) are
   good candidates for the context.

Real World Example: Context in Tideways
---------------------------------------

How to introduce such a context? We could create an object in our application,
for example how we did it in `Tideways <https://tideways.io>`_
with selected tenant (organization), application, date-range and server environment:

.. code-block:: php

    <?php

    class PageContext
    {
        /**
         * @var \Xhprof\Bundle\OrganizationBundle\Entity\Organization
         */
        private $organization;

        /**
         * @var \Xhprof\Bundle\OrganizationBundle\Entity\Application
         */
        private $application;

        /**
         * @var \Xhprof\Common\Date\DateRange
         */
        private $selectedDateRange;

        /**
         * @var \Xhprof\Bundle\ProfilerBundle\View\EnvironmentView
         */
        private $selectedEnvironment;

        // constructor and getters
    }

This object is created during request boot, in my case with a framework
listener. The listener checks for access rights and security constraints,
showing the 403/access denied page when necessary. This make 90% of access
control checks unneeded that are usually cluttering the controller.

The context is then made available for the application by using a Symfony
`parameter converter
<https://www.beberlei.de/2013/02/19/extending_symfony2__paramconverter.html>`_, every controller-action can get access to the context
by type-hinting for it:

.. code-block:: php

    <?php

    class ApplicationController
    {
        public function showAction(PageContext $pageContext)
        {
            return array('application' => $pageContext->getApplication());
        }
    }

The beauty of this approach is avoiding global state and passing
the context around in a non-singleton way. Depending on the framework
you use, it might be hard to achieve this kind of context injection.

Now when I build `lightweight Symfony2 controllers
<https://www.beberlei.de/2014/10/14/lightweight_symfony2_controllers.html>`_
in my applications, using a context object allows me to use even less services
and move repetitive find and access control code outside of the controllers.

I have also written a Twig extension that gives me access to the context
object, so I don't have to return it from every controller and created
a wrapper for the URL Generation that appends context information
to every URL (current date range + environment):

.. code-block:: jinja2

    <h1>{{ pageContext.application.name }}</h1>

    <a href="{{ page_path("some_route") }}">Link with Context query arguments</a>

Conclusion
----------

A context object can help you make global state explicit and control access to
it. Good requirements for a context object are immutability and not being a
singleton.

When used correctly this pattern can save you alot of redundant code and
simplify both controllers and views massively.

The pattern has its drawbacks: You have to be careful not put too powerful
objects into the context and if you can modify the context, then you will
probably introduce nasty side effets at some point. Additionally if you don't
make sure that creating the context is a very fast operation then you will
suffer from performance hits, because the context is created on every request,
maybe fetching expensive data that isn't even used.

.. author:: default
.. categories:: none
.. tags:: Symfony, DesignPatterns, ApplicationDesign
.. comments::
