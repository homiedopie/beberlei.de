Service Layers Mistakes: No central dispatching
===============================================

One benefit of recent applications over old 90s, early 2000 style PHP is
central dispatching of requests through one `Application` or `Dispatcher`
object. This is true for dispatching objects such as PHPs `SoapServer` or
`Zend\XmlRpc\Server` as well. Old style applications use the
webserver (Apache, Nginx) for the dispatching of routes to executed PHP
scripts.

Central dispatching allows developers to hook into central events during the
request processing to implement security, routing, caching, debugging, logging,
localization and many things more transparently.

If you check this list of features, these are all cross-cutting concerns to
the real purpose of your application and nicely abstracted from the core
of your application using central dispatching.

When building a future proof system focussing on the domain and starting
test-driven without a UI, it makes sense to use `Service Layer Pattern
<http://martinfowler.com/eaaCatalog/serviceLayer.html>`_ to decouple our
business logic from nasty technical decisions such as what framework to use, if
the application is served via REST API or directly renders to HTML, maybe even
works over different protocols. The service layer however is affected by the
same cross cutting concerns again. A language with support for
Aspect-Oriented-Programming could handle those concerns nicely, but PHP is not
such a language.

Service Layer without Dispatching
---------------------------------

As a practical example I will pick the classical user registration example,
starting with a service-layer that implements the cross-cutting
concerns inside the service method:

.. code-block:: php

    <?php

    class UserService
    {
        public function create($email, $password)
        {
            $this->security->assertNotLoggedInAlready();

            $user = new User();
            $user->setEmail($email);
            $user->encodePassword($password);

            $violations = $this->validator->validate($user);

            if (count($violations) > 0) {
                throw new \IllegalArgumentException(((string)$violations);
            }

            $this->entityManager->persist($user);
            $this->entityManager->flush();

            $message = "Thanks for registering! Please click here: ...";
            $this->mailer->sendMessage($email, $message);

            $this->logger->info("New user registration: " . $email);
        }
    }

This is quickly getting out of hands with the number of services needed
and you will not have fun testing this for example. This approach
violates the Single-Responsibility-Princple (SRP) doing way too much
non-related operations.

Using the Decorator Pattern
---------------------------

We could use the decorator pattern to extract some of the cross-cutting concerns
into their own services. This requires to introduce an interface for ``UserService``
and then building decorators for the different concerns. Then the service
can be built as a decorator chain:

.. code-block:: php

    <?php

    $userService =
        new LogUserService(
            new SecurityUserService(
                new DoctrineTransactionUserService(
                    new UserService(), ...
                ), ...
            ), ...
        );

The real ``UserService`` will slimmer and more closely handling just the
business logic related information. But this solution with decorators **does
not scale**, our service layer probaly needs a lot of methods. We would need to
write this **for every** method on every service, introducing many decorators
and interfaces that duplicate lots of code.

Introducing a Dispatcher
------------------------

Lets refactor from decorator towards a dispatching approach instead, to
keep more reusable. The ``CommandDispatcher`` object accepts a service name
and method and calls it. We can wrap every call with cross-cutting
concerns.

Starting with the most simple dispatcher possible, by just delegating the calls,
we add all the cross-cutting concerns. Note: This is **deliberatly written
without further abstraction**, just to show the concept. The real thing would
propably seperate the responsibilities from each other.

.. code-block:: php

    <?php

    class CommandDispatcher
    {
        private $services;

        public function registerService($serviceName, $service)
        {
            $this->services[$serviceName] = $service;
        }

        public function execute($serviceName, $method, array $params)
        {
            $service = $this->services[$serviceName]; // make lazy
            $callback = array($service, $method);

            if ($serviceName === "user" && $method === "create") {
                $this->assertNotLoggedInAlready();
            }

            $this->entityManager->beginTransaction();
            try {

                $result =  call_user_func_array($callback, $params);
                $this->entityManager->commit();

                $this->mailer->sendQueuedMails(); // "deferred commit" of mails
                $this->logger->info("Called $serviceName.$method");

            } catch (\Exception $e) {
                $this->entityManager->rollBack();
                throw $e;
            }

            return $result;
        }
    }

The dispatcher handles transactions around all the commands and also makes sure
that when they send emails, those only get send when the transaction was
successful. It checks if the user has the correct access
controls/authentication and performs some generic logging.

And using the dispatcher in your code looks like this:

.. code-block:: php

    <?php
    $dispatcher = new CommandDispatcher();
    $dispatcher->registerService('user', new UserService());

    $dispatcher->execute('user', 'create', array($email, $password));

Like the front controller in MVC or PHPs ``SOAPServer`` you register
services/functions with the dispatcher. Registration of services can be done by
convention, via some DependencyInjection Container Service name or any other
way you prefer. The dispatcher then handles ALL commands by wrapping them
inside some generic logic.

Compared to the Decorator approach, you can now easily reuse this code with
many commands. Except registering new services, no new code is necessary when
adding a new method or service.

A better API for the Dispatcher
-------------------------------
    
So far the API of the dispatcher is tedious, so lets work a little bit on how
you actually call methods on the service-layer.

There are two ways to make this call nicer. The first is use magic ``__call`` and some
clever duck-typing to create an API similar to this:

.. code-block:: php

    <?php

    $dispatcher = new CommandDispatcher();
    $dispatcher->registerService('user', new UserService());

    $dispatcher->user()->create($email, $password);

The second approach does not require magic ``__call``, but requires you to write a class for each
command. We map the command class name to a callback:

.. code-block:: php

    <?php

    $userService = new UserService();

    $dispatcher = new CommandDispatcher();
    $dispatcher->registerCommand('CreateUserCommand', array($userService, 'create'));

    $dispatcher->handle(new CreateUserCommand($email, $password));

The naming is very techincal here, but since the dispatcher also acts as a
facade to the application, we could give it better names like
``PayrollApplication``, ``Shop``, ``TrackingSystem``, any name the application
has inside your organization.

Discussion
----------

Now that I have shown the implementation of a dispatcher a small discussion
is necessary to evaluate it. The cross-cutting concerns could be nicely
wrapped in the dispatcher, so we achieved a considerable improvement
over the first example with all the concerns nicely seperated from each other.

The benefits are:

- Services themself don't need access to the cross-cutting concerns anymore,
  reducing the number of dependencies and increasing maintainability and
  testability.

- Handling cross-cutting concerns, that can make the service layer code very
  complex otherwise, in a clean way
  
- All the concerns are easily composable and the result is a SOLID approach towards them.

- The dispatcher also allows us to add or remove concerns later at one central
  location without having to change all the service layer code.

- The framework we use can be very simple as long it fullfils the major
  requirement to be easily compatible to the dispatcher approach.

How do we use this dispatcher in our MVC framework though? Instead of using
controllers/actions a REST or SOAP API could just use the dispatching and
services directly and map the HTTP request to it based on convention. This
would be a real win and simplify the framework-glue code considerably.

In a web-application however this is not so simple. We need to send redirects,
manage session state and handle request and response data, which often requires one
specific controller-action for each command. With some experimentation
it might be possible to achieve a much higher re-use here, but it might fail as
well.

That brings us to the downside of the dispatcher approach:

- We need some additional code and extra classes, which might be too much for
  small applications and the indirection of handling cross-cutting concerns
  might confuse teammates. 

- Having the dispatcher object inside controllers feels strange from the MVC
  point of view, it doesn't really fit. It also still may require implementing
  one action for every command, not simplifying this part of the development.

- While other languages don't need this because of their support for AOP and
  annotations (Spring for Java for example) this is necessary in PHP only,
  because we don't have this features.

- Unless we use the explicit command object approach, there is no
  auto-completion for commands on the dispatcher in the IDEs.

My conclusion from working with both kind of service layers: If you decided for
such a service layer, then my experience shows it is a mistake not to use a
dispatcher, because the benefits outweigh the downsides.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
