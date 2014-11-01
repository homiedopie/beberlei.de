Lightweight Symfony2 Controllers
================================

For quite some time I have been experimenting how to best implement Symfony 2
controllers to avoid depending on the framework. I have discussed many of these
insights here in my blog.

There are three reasons for my quest:

Simplicity: Solutions to avoid the dependencies between framework
and your model typically introduce layers of abstraction that produce
complexity. Service layers, CQRS and various design patterns are useful
tools, but developing every application with this kind of abstraction screams
over-engineering.

While the Domain-Driven Design slogan is "Tackling complexity in software",
there are many abstractions out there that can better be described as "Causing
complexity in software". I have written some of them myself.

Testability: There is a mantra "Don't unit-test your controllers" that arose
because controllers in most frameworks are just not testable. They have many
dependencies on other framework classes and cannot be created in a test
environment. This lead many teams to use slow and brittle integration tests instead.

But what if controllers were testable because they don't depend on the
framework anymore. We could avoid testing all the many layers that we
have removed for the sake of simplicity and also reduce the number of
slow integration tests.

Refactorability: I found that when using service layer or CQRS, there is a
tendency to use them for every use-case, because the abstraction is in place.
Any use-case that is not written with those patterns is coupled against the
framework again. Both development approaches are very different and refactoring
from one to the other typically requires a rewrite.

A good solution should allow refactoring from a lightweight controller to a
service layer with a small number of extract method and extract class
refactorings.

While working on the `Qafoo PHP Profiler <https://qafoolabs.com/>`_ product I
went to work on a solution that allowed for Simplicity, Testability and
Refactorability and came up with the
`NoFrameworkBundle <https://github.com/qafoolabs/QafooLabsNoFrameworkBundle>`_.

The design of the bundle is careful to extend Symfony in a way that is easy
for Symfony developers to understand. To achieve this it heavily extends
upon the FrameworkExtraBundle that is bundled with Symfony.

The design goals are:

- Favour Controller as Services to decouple them from the Framework.
- Replace every functionality of the Symfony Base controller in a way
  that does not require injecting a service into your controller.
- Never fetch state from services and inject it into the controller instead.
- Avoid annotations

The concepts are best explained by showing an example:

.. code-block:: php

    <?php

    use QafooLabs\MVC\TokenContext;

    class TaskController
    {
        private $taskRepository;

        public function __construct(TaskRepository $taskRepository)
        {
            $this->taskRepository = $taskRepository;
        }

        public function showAction(TokenContext $context, Task $task)
        {
            if (!$context->isGranted('ROLE_TASK', $task)) {
                throw new AccessDeniedHttpException();
            }

            return array('task' => $task);
        }
    }

This example demos the following features:

- The ``TokenContext`` wraps access to the ``security.context`` service and is
  used for checking access permissions and retrieving the current User object.
  It is passed to the controller with the help of ParamConverter feature.

  ``TokenContext`` here is just an interface and for testing you can 
  use a very simple mock implementation to pass an authenticated user to your
  controller.

- View parameters are returned from the controller as an array, however
  without requiring the ``@Template`` annotation of the
  SensioFrameworkExtraBundle.

The next example demontrates the abstraction for form requests that help writing very
concise form code:

.. code-block:: php

    <?php

    use QafooLabs\MVC\TokenContext;
    use QafooLabs\MVC\RedirectRouteResponse;
    use QafooLabs\MVC\FormRequest;

    class TaskController
    {
        private $taskRepository;

        public function newAction(FormRequest $formRequest, TokenContext $context)
        {
            $task = new Task($context->getUser());

            if ($formRequest->handle(new TaskType(), $task)) {
                $this->taskRepository->save($task);

                return new RedirectRouteResponse('Task.show', array('id' => $task->getId()));
            }

            return array('form' => $formRequest->createFormView());
        }
    }

- The ``RedirectRouteResponse`` is used to redirect to a route without
  a need for the ``router`` service.

- Usage of the ``FormRequest`` object that is a wrapper around FormFactory and
  Request object. It is passed by using a ParamConverter. The method
  ``$formRequest->handle`` combines binding the request and checking for valid
  data.

  Again there is a set of mock form request that allow you to simulate valid or
  invalid form requests for testing.

Writing controllers in this way addresses my requirements Simplicity,
Testability and Refactorability. For simple CRUD controllers they only ever
need access to a repository service. If one of your controllers grows too big,
just refactor out its business logic into services and inject them.

Check out the `repository on Github
<https://github.com/QafooLabs/QafooLabsNoFrameworkBundle>`_ for some more
features that we are using the `Profiler <https://qafoolabs.com/>`_.

Update 1: Renamed ``FrameworkContext``to ``TokenContext`` as done
in new 2.0 version of the bundle.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
