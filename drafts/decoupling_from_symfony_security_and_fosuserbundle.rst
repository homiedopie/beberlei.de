Decoupling from Symfony Security and FOSUserBundle
==================================================

In this blog post I will show how to decouple your core application
from the Symfony Security component and User bundles such as the FOSUserBundle.

In my opinion a framework has to be evaluated by how much it allows you to hide
it from your actual application. This blog post will add another perspective on
how to achieve decoupling from Symfony user and security with a very simple
approach. With this puzzle piece and others I wrote about before (`Controllers
as Service
<http://whitewashing.de/2013/06/27/extending_symfony2__controller_utilities.html>`_,
`Param Converters
<http://whitewashing.de/2013/02/19/extending_symfony2__paramconverter.html>`_)
and other pieces I still need to write about, I would classify Symfony2 as a
good framework.

A number of other authors have written blog posts on decoupling Symfony and your model
code as well, such as William Durand `on project structure
<http://williamdurand.fr/2013/08/07/ddd-with-symfony2-folder-structure-and-code-first/>`_
, Matthias Verraes `on project structure as well <http://verraes.net/2011/10/code-folder-structure/>`_
and on `Decoupling Forms from Entities
<http://verraes.net/2013/04/decoupling-symfony2-forms-from-entities/>`_.

User management breaks the isolation of your business model open,
by introducing the ``UserInterface`` from the Security component into your
code base. In combination with the *FOSUserBundle* this can cause a dependency
on quite a bit of code already because the ``FOS\UserBundle\Model\User`` object
cannot be called leightweight. However this and other FriendsOfSymfony bundles
are very helpful to get annoying features of your application done in a matter
of hours.

You can decouple the *FOSUserBundle* from our own entities and code by
introducing a second object that representes the user concept in our model.
The ``UserInterface`` entities need fields for username, password, enabled and
some more. Except the username and email, the business model rarely needs other
properties.

Take an ecommerce system as example, where customers can register as users.
In this example we could create two entities ``MyProject\UserBundle\Entity\User`` and
``MyProject\ShopBundle\Entity\Customer``. Two strategies exist now:

1. Use the same table for both entities with some shared and other exclusive columns
2. Use different tables in the database

I haven't tried the first option yet, so I cannot say much about the feasibility.

For case two, the ``User`` entity looks like this:

.. code-block:: php

    <?php
    // src/MyProject/UserBundle/Entity/User.php;

    namespace MyProject\UserBundle\Entity;

    use FOS\UserBundle\Model\User as BaseUser;
    use Doctrine\ORM\Mapping as ORM;

    /**
     * @ORM\Entity
     * @ORM\Table(name="fos_user")
     */
    class User extends BaseUser
    {
        /**
         * @ORM\Id
         * @ORM\Column(type="integer")
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;
    }

The ``Customer`` entity is a completly new object, not depending
on the ``UserInterface`` and containing some duplicated properties.

You can either use exactly the same ID or plant the ``$userId`` as
correlation ID in the ``Customer`` object.

.. code-block:: php

    <?php
    // src/MyProject/ShopBundle/Entity/Customer.php

    namespace MyProject\ShopBundle\Entity;

    use Doctrine\ORM\Mapping as ORM;

    /**
     * @ORM\Entity
     * @ORM\Table(name="customer")
     */
    class Customer
    {
        /**
         * @ORM\Id
         * @ORM\Column(type="integer")
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        /**
         * @ORM\Column(type="string")
         */
        protected $username;
    }

Now you need to extend the application to synchronize all changes from the
``User`` entity to the ``Customer`` entity. From my experience this can be
achieved relatively easy by overwriting the ``ModelManager`` or when finally
supported by *FOSUserBundle* listening to events.  Your own code can
exclusively work with ``Customer`` objects.

.. author:: default
.. categories:: PHP, Symfony2
.. tags:: PHP, Symfony2
.. comments::
