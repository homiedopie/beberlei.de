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
        protected function removeEntity($class, $id)
        {
            $entityManager = $this->get('doctrine.orm.default_entity_manager');
            $user = $entityManager->find($class, $id);

            $entityManager->remove($user);
            $entityManager->flush();
        }
    }


.. author:: default
.. categories:: none
.. tags:: none
.. comments::
