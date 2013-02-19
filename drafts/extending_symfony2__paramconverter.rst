Extending Symfony2: ParamConverter
==================================

Symfony2 is an extremly extendable framework, everything is extendable or
overwritable through the Dependency Injection Container. The problem developers
face is knowing about the extension points and when to use them.  If you don't
know the extension points, your Symfony application will end up with code
duplication, too much inheritance and very little unit-testable code.

This blog post will be the first in a series, describing Symfony2 extension
points that help you achieve clean and duplicateless code. In my experience,
using Symfony extension points to avoid code duplication helps you avoid
writing thousands of lines of code in your controllers.

The problem: Duplicate finder logic
-----------------------------------

Inside controllers you can easily end with lots of duplication using the same
general finder logic again in several actions. Take this following example:

.. code-block:: php

    <?php
    class UserController extends Controller
    {
        public function showAction($id)
        {
            $dql = "SELECT u, d, a
                      FROM MyBundle\Entity\User u
                      JOIN u.details d
                      JOIN u.addresses a
                      WHERE u.id = ?1";

            $user = $this->get('doctrine.orm.default_entity_manager')
                ->createQuery($dql)
                ->setParameter(1, $id)
                ->getSingleResult();

            if ( ! $user) {
                throw new NotFoundHttpException();
            }

            return array('user' => $user);
        }
    }

If we need this block of code in several actions of different controllers, we
will end up with duplication that has to be eliminated.

The Quick and Dirty Solution
----------------------------

One way of resolving the duplication appearing in this case, is moving the
finder + not found logic into a common controller base class or into a trait.
But this leaves us with a helper method buried in the code and a static
dependency to a base class or a trait that we want to avoid.

.. code-block:: php

    <?php
    class AbstractController extends Controller
    {
        protected function findUser($id)
        {
            $dql = "SELECT u, d, a
                      FROM MyBundle\Entity\User u 
                      JOIN u.details d
                      JOIN u.addresses a
                      WHERE u.id = ?1";

            $user = $this->get('doctrine.orm.default_entity_manager')
                ->createQuery($dql)
                ->setParameter(1, $id)
                ->getSingleResult();

            if ( ! $user) {
                throw new NotFoundHttpException();
            }

            return $user;
        }
    }

There are two problems with this sort of refactoring:

1. We are using inheritance for code-reuse.
2. We hide the ``findUser`` behavior in an abstract class and make it hard to test.

The Preferred Solution
----------------------

The `SensioFrameworkExtraBundle
<http://symfony.com/doc/current/bundles/SensioFrameworkExtraBundle/annotations/converters.html>`_
offers an extension hook called **Parameter Converters** to transform Request
attributes to objects directly for controller method arguments. They hook into
the ``kernel.controller`` event that you can use yourself to achieve the same
goal.

Lets see how the action will look like after our refactoring:

.. code-block:: php

    <?php
    class UserController extends Controller
    {
        public function showAction(User $user)
        {
            return array('user' => $user);
        }
    }

Very concise and easy to read. The param converter doing the heavy lifting
looks like this:

.. code-block:: php

    <?php
    namespace MyProject\Request\ParamConverter;

    use Sensio\Bundle\FrameworkExtraBundle\Configuration\ConfigurationInterface;
    use Sensio\Bundle\FrameworkExtraBundle\Request\ParamConverter\ParamConverterInterface;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
    use Doctrine\ORM\EntityManager;

    class UserParamConverter implements ParamConverter
    {
        private $entityManager;

        public function __construct(EntityManager $entityManager)
        {
            $this->entityManager = $entityManager;
        }

        public function apply(Request $request, ConfigurationInterface $configuration)
        {
            $id = $request->attributes->get('id');

            $dql = "SELECT u, d, a
                      FROM MyBundle\Entity\User u
                      JOIN u.details d
                      JOIN u.addresses a
                      WHERE u.id = ?1";

            $user = $this->get('doctrine.orm.default_entity_manager')
                ->createQuery($dql)
                ->setParameter(1, $id)
                ->getSingleResult();

            if ( ! $user) {
                throw new NotFoundHttpException();
            }

            $param = $configuration->getName();
            $request->attributes($param, $user);

            return true;
        }

        public function supports(ConfigurationInterface $configuration)
        {
            return "MyProject\Entity\User" === $configuration->getClass();
        }
    }

Now we only need to register this class in the dependency injection container:

.. code-block:: xml

    <service id="my_project.user_param_converter"
          class="MyProject\Request\ParamConverter\UserParamConverter">
        <argument type="service" id="doctrine.orm.default_entity_manager" />

        <tag name="request.param_converter" converter="user" priority="10" />
    </service>

With the priority configuration the ``User`` entity is now alway handled
by our custom param converter and not by the default Doctrine converter.

In a next step, we should extract the query logic from the ParamConverter
into a custom Doctrine entity repository. But that is a task for another blog
post in this series.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
