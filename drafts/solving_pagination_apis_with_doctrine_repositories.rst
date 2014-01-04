Solving Pagination APIs with Doctrine Repositories
==================================================

For quite some time now it bugs me that existing pagination APIs are
violating decoupling in MVC. One example where this is clearly happening is
when you are using KnpLabs Pager in combination with Solarium. In that
case the ``Paginator#paginate()`` method requires an array of ``$select`` and
``$solrClient``. Integrations for the Doctrine ORM require to pass Query or
QueryBuilder objects for both Pagerfanta and KnpLabs Pager.

If you integrate with those APIs, then you have to do this inside of your
Repository or DAO (data-access-object) and return the paginated data. However
in that case you need multiple APIs for returning data paginated and
non-paginated, which is very inconvenient and annoying. In any way you
have to provide an interface for the repository that returns information
about the datasource.

To solve this problem we need a pagination API that allows both paginated
and non-paginated iteration. This API has to hide the internals of the
datasource itself, so that you can freely pass it from a repository/DAO into
the rest of your code (model, controller and view).

Because I keep stumbling accross this missing API issue, I took the time to
come up with a simple that allows me to better seperate the concern of
pagination in my applications. `Alexander <https://twitter.com/iam_asm89>` gave
me a hard time on the API design, so hopefully something good came out.

I dubbed this library `Porpaginas <https://github.com/beberlei/porpaginas>`_
which means "by page" in english or "seitenweise" in german and released
a first version on Github.

For now it will only work with the Doctrine ORM or an in memory array
implementation. The primary API is the interface ``Porpaginas\Result``.
From your repository or DAO objects you return an implementation of this
interface.

.. code-block:: php

    <?php

    namespace Acme\DemoBundle\Entity;

    use Porpaginas\Doctrine\ORM\ORMQueryResult;
    use Doctrine\ORM\EntityRepository;

    class UserRepository extends EntityRepository
    {
        /**
         * @return \Porpaginas\Result
         */
        public function findAllUsers()
        {
            $qb = $this->createQueryBuilder('u')->orderBy('u.username');

            return new ORMQueryResult($qb);
        }
    }

Now there are two ways of dealing with an instance of ``Porpaginas\Result``.
You can either

1. iterate it directly and retrieve the complete result of the query.
2. call the method ``take($offset, $limit)`` to create a paginator for the
   query.

This way the client has full control over the decision to paginate or not and
you don't have to think about this in the API of the repository/DAO.

.. code-block:: php

    <?php

    $userResult = $userRepository->findAllUsers();

    foreach ($userResult as $user) {
        // all users here
    }

    foreach ($userResult->take(0, 20) as $user) {
        // only the first 20 users
    }

Porpaginas API alone does solve the full pagination equation, you also need to
integrate with some API to render the page numbers and generate urls the right
way. To avoid reinventing the wheel, integration with Pagerfanta or KnpLabs
Pager is part of the package. That means you can pass a ``Porpaginas\Page``
object that is returned from ``take($offset, $limit)`` and pass it to Twig,
where a helper exists to render the pagination with either of the two
libraries:

.. code-block:: jinja

    We found a total of <strong>{{ porpaginas_total(users) }}</strong> users:

    <ul>
    {% for user in users %}
        <li>{{ user.name }}</li>
    {% endfor %}
    </ul>

    {{ porpaginas_render(users) }}

This probably only solves rendering for the Symfony and related ecosystems,
however that is the one I care about at the moment. You can of course provide
your own rendering and integrate into your framework and work with the ``Page``
API to do so.  Maybe in the future this library will have its own rendering
engine, at the moment it is good enough for me.

Go grab your copy with Composer:

.. code-block:: json

    {
        "require": {
            "beberlei/porpaginas": "dev-master"
        }
    }

Please post feedback and issues in the comments or into the `Github issue
tracker <https://github.com/beberlei/porpaginas/issues>`_.

.. author:: default
.. categories:: PHP
.. tags:: PHP, Porpaginas
.. comments::
