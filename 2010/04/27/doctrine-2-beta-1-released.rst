
Doctrine 2 Beta 1 released
==========================

Today we are happy to announce that the first beta of `Doctrine
2 <http://www.doctrine-project.org/blog/doctrine-2-0-0-beta1-released>`_
has been released and we fixed 165 issues kindly reported by several
early adopters.

You can grab the code from the Github project:

    `http://github.com/doctrine/doctrine2/tree/2.0.0-BETA1 <http://github.com/doctrine/doctrine2/tree/2.0.0-BETA1>`_
     git clone git://github.com/doctrine/doctrine2.git

Or download it from our website:

    `http://www.doctrine-project.org/download#2\_0 <http://www.doctrine-project.org/download#2_0>`_

It is our believe that Doctrine 2 brings PHP ORMs to a new level. We are
leaving behind the Active Record pattern because we think it hurts
testability, project maintainability and is not a suitable abstraction
(80/20) for models that exceed the complexity of a blog or otherwise
simple web application. Instead we implemented a pure Data Mapper
approach with help of the new Reflection functionalities of PHP 5.3, so
your Domain Objects neither have to extend a base class nor implement an
interface.

We also dropped most of the magical features of Doctrine 1 in favour of
a simple and standardized API that is loosely based on the `Java
Persistence API <http://en.wikipedia.org/wiki/Java_Persistence_API>`_, a
technical standard for Object Relational Mappers. However we try not to
blindly follow the "Programm PHP like Java" approach and and deviated
from JPA where applicable to make the concepts fit better into the PHP
environment, such as alternatively hydrating all results into nested
array structures for very high read performance.

The cornerstone of Doctrine 2 is the query language DQL. It allows to
execute queries on the object level defined by your metadata in a
similar fashion to SQL. You can even do Joins, Subselects and Aggregates
and Group Clauses in DQL, eliminating the need to circumvent ORMs for
more advanced SQL features. Nevertheless it is also possible to write
plain SQL and let Doctrine 2 hydrate the results into an object graph.

In the last three month since alpha 4 we have done considerable changes
and integrated lots of feedback from our users. The most notable changes
are:

-  Allowing Constructors of your Domain Objects to have non-optional
   parameters.
-  Allow to define a natural ordering of to Many Collections that is
   automatically enforced trough an SQL ORDER BY statement when
   retrieved from the database.
-  Shipping the Symfony Console Component to replace our own Console
   Implementation
-  New DQL syntax to load objects partially, omitting potentially
   expensive fields from retrieval for the current request.
-  Changes to how bi-directional have to be defined in the mapping
   files.
-  Several changes to the Events API inside the ORM, to make sure many
   possible extension scenarios work smoothly.
-  Enhancements to our Console Tools
-  Surpassed the 1000 unit-tests each running against Postgres, Mysql,
   Sqlite and Oci8 drivers.
-  Moved from SVN to Git:
   `http://github.com/doctrine/doctrine2 <http://github.com/doctrine/doctrine2>`_

We also did several painful backwards incompatible changes that seemed
necessary to clean up and optimize the API or allow the ORM to be even
faster than before. The beta phase beginning today will not contain any
larger BC breaks anymore, opening up this release for a broader testing
audience.

For the next iteration several enhancements are planned:

-  Support for PDO IBM, IBM DB2, SqlSrv and PDO SqlSrv und MsSql drivers
-  Pessimistic Lock Support (FOR UPDATE and SHARED)
-  Support for Custom Hydration Modes
-  Support for Custom Persister Implementations
-  Support for handling very large collections of related objects
   without needing an in-memory representation of the collection
-  Separation of Doctrine\\Common, Doctrine\\DBAL and Doctrine\\ORM into
   three different projects
-  Extend the documentation even further, adding quickstart tutorials,
   cookbook recipes and enhancing the existing chapters.

We also plan to support several extensions for the 2.0 release such as:

-  Migrations
-  PHPUnit Database Testing Integration
-  NestedSet Support
-  Symfony 2 Support
-  Zend Framework 2 Support

Please try out the new Beta release If you find the time and leave your
feedback in our `Issue
Tracker <http://www.doctrine-project.org/jira/secure/Dashboard.jspa>`_,
the `Mailing-List <http://groups.google.com/group/doctrine-user>`_ or
come discuss with us on Doctrine 2 on Freenode #doctrine-dev.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>