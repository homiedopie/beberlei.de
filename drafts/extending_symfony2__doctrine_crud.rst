Extending Symfony2: Doctrine ClassMetadata
==========================================

When writing CRUD applications sticking to the Symfony default workflow of
writing controllers is going to be a huge timewaster. To develop reusable
controllers and actions you should to make yourself familiar with Doctrine
ClassMetadata, which allows you to write reusable actions for Doctrine (ORM or
ODMs work the same).

The problem: Dupliate code in controllers
-----------------------------------------

CRUD Actions look the same for Doctrine entities most of the time. Take
this remove action:

.. code-block:: php

    <?php
    class UserController extends Controller
    {
        public function removeAction(Request $request)
        {
            $id = $request->attributes->get('id');
            $entityManager = $this->get('doctrine.orm.default_entity_manager');
            $user = $entityManager->find('Acme\UserBundle\Entity\User', $id);

            $entityManager->remove($user);
            $entityManager->flush();

            return $this->redirect($this->generateUrl('user_list'));
        }
    }

We need the same block of code for every entity that is removable.
And just these lines will probably not be enough, missing here is:

- Security checks
- Post processing
- Flash messages (and translations)

In a few more minutes we can probably come up with more possible requirements.

The Quick and Dirty Solution
----------------------------

Inheritance is the simple way out of this problem, we can write a CRUD
Controller that solves the problem:

.. code-block:: php

    <?php
    abstract class CRUDController extends Controller
    {
        abstract public function getEntityClass();

        abstract public function getEntityListRouteName();

        public function removeAction(Request $request)
        {
            $id = $request->attributes->get('id');
            $entityManager = $this->get('doctrine.orm.default_entity_manager');
            $entity = $entityManager->find($this->getEntityClass(), $id);

            $entityManager->remove($entity);
            $entityManager->flush();

            return $this->redirect($this->generateUrl($this->getEntityListRouteName()));
        }
    }

And you can implement this base controller to solve the User example from
above:

.. code-block:: php

    <?php
    class UserController extends CRUDController
    {
        public function getEntityClass()
        {
            return 'Acme\UserBundle\Entity\User';
        }

        public function getEntityListRouteName()
        {
            return 'user_list';
        }
    }

The clean solution: Controller Helper
-------------------------------------

The problem with the quick and dirty solution is its violation of the single
responsibility and the interface seggregatoin principle.  The
``CRUDController`` class will become huge once you start adding all the
different actions, for example batch operations on the list and so on.
Additionally not all the Doctrine entities will require ALL the actions,
but some only need a subset.

Instead of cramping all the stuff into one big class, lets introduce
helper classes for each operation:

.. code-block:: php

    <?php
    namespace Acme\UserBundle\Controller\Helper;

    class DeleteEntity
    {
        private $entityManager;

        public function __construct(EntityManager $entityManager)
        {
            $this->entityManager = $entityManager;
        }

        public function remove($class, $id, $redirectUri, array $redirectParams = array())
        {
            $entity = $this->entityManager->find($class, $id);

            $this->entityManager->remove($entity);
            $this->entityManager->flush();

            return $this->redirect($this->generateUrl($redirectRoute, $redirectParams));
        }
    }

And after registering this helper in the DIC, for example as ``acme_demo.controller_helper.delete_entity``,
you can use it in every controller as you wish:

.. code-block:: php

    <?php
    namespace Acme\UserBundle\Controller;

    class UserController extends CRUDController
    {
        public function removeAction(Request $request)
        {
            return $this->get('acme_demo.controller_helper.delete_entity')
                ->remove(
                    'Acme\UserBundle\Entity\User',
                    $request->attributes->get('id'),
                    'user_list'
                );
        }
    }

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
