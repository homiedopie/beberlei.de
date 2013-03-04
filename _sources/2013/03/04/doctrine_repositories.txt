========================================
On Taming Repository Classes in Doctrine
========================================

Over at the `easybib/dev
<http://drafts.easybib.com/post/44139111915/taiming-repository-classes-in-doctrine-with-the>`_
Blog Anne posted an entry about their usage of Doctrine Repositories with a
growing amount of query responsibilities. I want to respond to this blog post
with two alternative approaches, because I have seen the easybib approach multiple
times in different projects by different teams and think it can be approved upon alot.

The problems with the approach outlined are:

- The Repository API does not hide implementation details of the ORM,
  the QueryBuilder API is returned to the client code. This might seen
  like nitpicking, however it leads to bloated client code doing the
  query builder work over and over again. For example the
  ``->getQuery()->getSingleResult(AbstractQuery::HYDRATE_ARRAY)`` call.

- Different parts of the QueryBuilder filtering cannot be composed together,
  because of the way the API is created. Assume we have the
  ``filterGroupsForApi()`` call, there is no way to combine it with another
  call ``filterGroupsForPermissions()``.  Instead reusing this code will lead
  to a third method ``filterGroupsForApiAndPermissions()``.
  
  This can lead to combinatorial explosion of methods that the developer using
  the repository needs to know.  And wading through a list of 100 methods to
  find the right one is never fun, most importantly when the naming of methods
  is imprecise.

Generally introducing a new object such as a repository should pass the
"`Composite is simpler than the sum of its parts
<http://www.growing-object-oriented-software.com/toc.html>`_" rule. However the
approach also clearly demonstrates a bad abstraction. In OOP the primary goal is avoiding
changes to affect the whole system.


Introduce Criteria Objects
--------------------------

Instead of using the ``QueryBuilder`` outside of the Repository, lets start with an
alternative refactoring. I will introduce a ``Criteria`` class for the ``User``:

.. code-block:: php

    <?php
    class UserCriteria
    {
        public $groupId;
        public $hydrateMode = Query::HYDRATE_OBJECT;
    }

It is important not to introduce a constructor here, because when we add
more and more criterions, the constructor will get bloated. Static
factory methods that create a criteria do make sense however.

Now we can introduce a ``match`` method on the ``UserRepository``. Lets see
that on an interface level first, to see how simple usage is for the client
side of the repository:

.. code-block:: php

    <?php
    interface UserRepository
    {
        /**
         * @param UserCriteria $criteria
         * @return array<User>|array<array>
         ***/
        public function match(UserCriteria $criteria);
    }

Put in a ``$criteria`` get back users or array data. Very nice and simple!
The implementation would look like this:

.. code-block:: php

    <?php
    /**
     * @param UserCriteria $criteria
     * @return array<User>
     ***/
    public function match(UserCriteria $criteria)
    {
        $qb = $this->createQueryBuilder('u');

        if ($criteria->groupId !== null) {
            $this->matchGroup($qb, $criteria);
        }

        return $qb->getQuery()->getResult($criteria->hydrateMode);
    }

    private function matchGroup($qb, $criteria)
    {
        $qb->where('u.group = :group')->setParameter(1, $criteria->groupId);
    }

The benefit here is, that we can add additional conditions and processing
by only adding a new property on the ``UserCriteria`` and then handling
this inside ``UserRepository#match()``. Additionally you can save the ``UserCriteria``
in the session, or even in the database to that users can "save filter" or return
to a search overview, with the previous criteria still known.

The client code now looks like:

.. code-block:: php 

    <?php
    $criteria = new UserCriteria();
    $criteria->groupId = $groupId;
    $criteria->hydrateMode = Query::HYDRATE_ARRAY;

    $groups = $app['orm.ems']['api']
        ->getRepository('EasyBib\Api\Entity\User')
        ->match($criteria);

What we achieved in this step, is a simple API for the developer using the
Repository and a simple way to compose conditions by setting new properties
in the criteria.

If you complain that the solution has the same amount of lines, than the
original EasyBib solution, then you are missing the point.  We have factored
away a violation of the Law Of Demeter and calls on an API (Doctrine)
that should be implementation detail of the repository.

Lets try this by adding a new filter criteria, for example permissions I mentioned before:

.. code-block:: php

    <?php
    class UserCriteria
    {
        const PERMISSION_READ = 'read';
        const PERMISSION_WRITE = 'write';
        //...
        public $permissions;
    }
    class UserRepository
    {
        public function match(UserCriteria $criteria)
        {
            // ...
            if ($criteria->permissions !== null) {
                $this->matchPermissions($criteria);
            }
            // ...
        }
    }

Simple enough, now we can use it everywhere we want by adding
for example ``$criteria->permissions = UserCriteria::PERMISSION_WRITE``
in our client code.

Specification Pattern
---------------------

The Criteria object gets us very far in abstracting lots of query building
behind a very simple API, but it fails short when:

- Composing Conditions using combinations of Not/And/Or is not possible
  without a tree structure, however ``Criteria`` is just a single object.

- Removing duplication of code between different repositories. If you
  have similar conditions, limit or ordering requirements then you can
  only solve this by having all repositories extend a base repository.
  But `Inheritance is evil <http://c2.com/cgi/wiki?ImplementationInheritanceIsEvil>`_.

The `Specfication pattern <http://en.wikipedia.org/wiki/Specification_pattern>`_ solves
this issue. There are several ways to implement it, in the spirit of refactoring I will
approach it from our existing Criteria.

Lets move the QueryBuilder code from the repository, into the Criteria object and
rename it ``UserSpecification``. Its important here to change the query builder
code to use expressions that can be composed.

.. code-block:: php

    <?php
    class UserSpecification
    {
        public $groupId;
        public $hydrateMode = Query::HYDRATE_OBJECT;
        public $permissions;

        public function match(QueryBuilder $qb, $dqlAlias)
        {
            $expr = "1=1";

            if ($criteria->groupId !== null) {
                $expr = $qb->expr()->and($expr, $this->matchGroup($qb));
            }

            if ($criteria->permissions !== null) {
                $expr = $qb->expr()->and($expr, $this->matchPermissions($qb));
            }

            return $expr;
        }

        public function modifyQuery(Query $query)
        {
            $query->setHydrationMode($this->hydrateMode);
        }

        private function matchGroup($qb)
        {
            $qb->setParameter('group', $this->groupId);

            return $qb->expr()->eq('u.group', ':group');
        }

        private function matchPermissions($qb)
        {
            // ...
        }
    }

The repository is then delegating the expression generation
and puts the result into the ``where()`` method of the builder

.. code-block:: php

    <?php
    class UserRepository
    {
        public function match(UserSpecification $specification)
        {
            $qb = $this->createQueryBuilder('u');
            $expr = $specification->match($qb, 'u');

            $query = $qb->where($expr)->getQuery();

            $specification->modifyQuery($query);

            return $query->getResult();
        }
    }

Stricly speaking, the ``UserSpecification`` violates the single reponsibility
principle, which prevents the composability of specifications and reuse in
different repositories. This is apparent by the ``$expr = "1=1";`` line that is
required to make the combination of conditions possible.
Lets factor away the violation of the single
responsibility principle by introducing three specifications:

.. code-block:: php

    <?php
    interface Specification
    {
        /**
         * @param \Doctrine\ORM\QueryBuilder $qb
         * @param string $dqlAlias
         * 
         * @return \Doctrine\ORM\Query\Expr
         ***/
        public function match(QueryBuilder $qb, $dqlAlias);

        /**
         * @param \Doctrine\ORM\Query $query
         ***/
        public function modifyQuery(Query $query);
    }

    class AsArray implements Specification
    {
        private $parent;

        public function __construct(Specification $parent)
        {
            $this->parent = $parent;
        }

        public function modifyQuery(Query $query)
        {
            $query->setHydrationMode(Query::HYDRATE_ARRAY);
        }

        public function match(QueryBuilder $qb, $dqlAlias)
        {
            return $this->parent->match($qb, $dqlAlias);
        }
    }

    class FilterGroup implements Specification
    {
        private $group;

        public function __construct($group)
        {
            $this->group = $group;
        }

        public function match(QueryBuilder $qb, $dqlAlias)
        {
            $qb->setParameter('group', $this->group);

            return $qb->expr()->eq($dqlAlias . '.group', ':group');
        }

        public function modifyQuery(Query $query) { /* empty ***/ }
    }

    class FilterPermission implements Specification
    {
        private $permissions;

        public function __construct($permissions)
        {
            $this->permissions = $permissions;
        }

        public function match(QueryBuilder $qb, $dqlAlias)
        {
            // ...
        }

        public function modifyQuery(Query $query) { /* empty ***/ }
    }

Now we need a new And-Specification to combine this in our code. This
looks rather abstract and complex on the inside, but for clients
of this object, the usage is simple and obvious.

.. code-block:: php

    <?php
    class AndX implements Specification
    {
        private $children;

        public function __construct()
        {
            $this->children = func_get_args();
        }

        public function match(QueryBuilder $qb, $dqlAlias)
        {
            return call_user_func_array(
                array($qb->expr(), 'andX'),
                array_map(function ($specification) use ($qb, $dqlAlias) {
                    return $specification->match($qb, $dqlAlias);
                }, $this->children
            ));
        }

        public function modifyQuery(Query $query)
        {
            foreach ($this->children as $child) {
                $child->modifyQuery($query);
            }
        }
    }

Assuming we import all specifications
from a common namespace ``Spec``, our client code will look
like this:

.. code-block:: php

    <?php
    $specification = new Spec\AsArray(new Spec\AndX(
        new Spec\FilterGroup($groupId),
        new Spec\FilterPermission($permission)
    ));

    $groups = $app['orm.ems']['api']
        ->getRepository('\EasyBib\Api\Entity\Group')
        ->match($specification);

In constrast to the criteria, we could now implement
or and not specifications to enhance query capabilities. 

Improving Specifications
------------------------

You can now introduce reusability accross different repositories by adding
functionality to check if a specification supports a given entity.

.. code-block:: php

    <?php
    interface Specification
    {
        // ..
        /**
         * @param string $className
         * @return bool
         ***/
        public function supports($className);
    }

Every composite can delegate this operation to its children, and every leaf of
the tree can return true or false. The Repository can then check for a valid
specification in its match method:

.. code-block:: php

    <?php

    abstract class EntitySpecificationRepository
    {
        public function match(Specification $specification)
        {
            if ( ! $specification->supports($this->getEntityName())) {
                throw new \InvalidArgumentExcetion("Specification not supported by this repository.");
            }

            $qb = $this->createQueryBuilder('r');
            $expr = $specification->match($qb, 'r');

            $query = $qb->where($expr)->getQuery();

            $specification->modifyQuery($query);

            return $query->getResult();
        }
    }

Now we can introduce very generic specifications, such as `OnlyPage($page, Specification $spec)``
for limit queries, or ``Equals($field, $value)``. For more readable code, you can then create
a domain language for your specifications that is composed of more simple specifications:

.. code-block:: php

    <?php
    class PowerUsers implements Specification
    {
        private $spec;

        public function __construct()
        {
            $this->spec = new OnlyPage(1, new AndX(
                new UsersWithInteraction(),
                new EnabledUsers(),
            ));
        }

        public function match(QueryBuilder $qb, $dqlAlias)
        {
            return $this->spec->match($qb, $dqlAlias);
        }

        public function modifyQuery(Query $query)
        {
            $this->spec->modifyQuery($query);
        }

        public function supports($className)
        {
            return ($className === 'EasyBib\Api\Entity\User');
        }
    }

    $top20powerUsers = new Spec\PowerUsers();

Hiding this kind of composition inside another specification allows
you to reuse query logic in different places in the application
easily and in terms of the domain language.

Testability of Doctrine Repositories
------------------------------------

One reasons outlined by Anne for this design is testability: Because the
Repository returns the QueryBuilder you have access to the generated SQL.
However testing Doctrine Repositories should never be verifying the generated
SQL. I see alot of people doing this and it is very fragile and dangerous.
Doctrine is a third party library and as such a rather complex one. Possible
changes that break the test are:

-  Doctrine adds/removes whitespaces to SQL in a next version
-  Doctrine performs SQL optimizations in certain cases, the result is the same though.
-  You add a field/column to any of the tables involved that does not affect the result.
-  You change something in the Doctrine mapping files, that leads to a reordering of SQL.

These are 4 changes that have absolutly nothing to do with the feature you are
actually testing, making the test code very fragile. In terms of abstraction
SQL generation is an implementation detail of the Doctrine ORM and you as
developer are only interested in the public API, which the SQL generation is
not part of.

The code should really be tested against Doctrine itself. Since you are using
Doctrine to get rid of SQL query generation for some use-cases, why should you
use them as measure of quality in your testing efforts. 

Testing repositories with the Specification pattern is testing the different
specifications in isolation against a real Doctrine database backend. This will
not be super simple to setup, but the isolation of specifications and their
reusability  accross repositories actually allows us to keep the number of
tests very small. The pattern avoids the problem of combinatorial explosion of
test-cases very neatly.

The real benefit of testabilty is achieved in tests of repository client code.
Before we were not able to unit-test this code, because of the Doctrine
EntityManager, Query + QueryBuilder dependencies.  Now We can inject the
repositories into our controllers and services and then use mock objects in the
tests.

.. author:: default
.. categories:: PHP
.. tags:: PHP
.. comments::
