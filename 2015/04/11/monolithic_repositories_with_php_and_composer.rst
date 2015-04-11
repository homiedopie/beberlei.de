Monolithic Repositories with PHP and Composer
=============================================

     tl;dr Monolithic repositories can bring a lot of benefits. I prototyped
     `Fiddler <https://github.com/beberlei/fiddler>`_ that complements Composer
     to add dependency management for monolithic repositories to PHP.

Thanks to `Alexander <https://twitter.com/iam_asm89>`_ for discussing this
topic with me as well as reviewing the draft of this post.

As Git and Composer are more ubiquitous in open-source projects and within
companies, monolithic repositories containing multiple projects have become a
bit of a bad practice. This is a similar trend to how monolithic applications
are out of fashion and the recent focus on microservices and Docker.

Composer has made it possible to create many small packages and distribute them
easily through Packagist. This has massively improved the PHP ecosystem by
increasing re-usability and sharing.

But it is important to consider package distribution and development seperate
from each other. The current progress in package manager tooling comes at a
cost for version control productivity, because Composer, NPM, Bower force you
to have exactly one repository for one package to benefit from the
reusability/distribution.

This blog post compares monolithic repositories with one repository per package
approach. It focuses on internal projects and repositories in organizations and
companies. I will discuss open source projects in a follow-up post.

Workflow at Facebook, Google, Twitter
-------------------------------------

The move towards smaller repositories is called into question by three extremely
productive organizations that work at incredible scale.

- Facebook `mentioned on their talk "Big Code: Developer Infrastructure at
  Facebook's Scale"
  <https://developers.facebooklive.com/videos/561/big-code-developer-infrastructure-at-facebook-s-scale>`_
  that they are going to merge their three big code repositories Server, iOS
  and Android into a single big repository over the course of 2015.

- Google open-sourced `Bazel <http://bazel.io>`_, the build tool behind a huge
  chunk of their codebase managed in a single Perforce repository with over 20 million
  commits (`Reference
  <http://www.perforce.com/sites/default/files/still-all-one-server-perforce-scale-google-wp.pdf>`_).

- Twitter, Foursquare and Square are working on their clone of Google's Bazels
  build system called `Pants <https://pantsbuild.github.io/>`_. It is also
  designed for monolithic repositories.

All three companies cite huge developer productivity benefits,
code-reusability, large-scale refactorings and development at scale for
choosing this approach. The Facebook talk even mentions how all their
development infrastructure efforts focus on keeping this workflow because of
the benefits it brings.

Downsides of having many Repositories
-------------------------------------

In contrast working with ever smaller repositories can be a huge burden for
developer mental models: I have seen this in open-source projects such as
Doctrine and several customer projects:

1. Cross repository changes require certain pull-requests on Github/Gitlab to
   be merged in order or in combination yet the tools don't provide visibility
   into these dependencies. They are purely informal, leading to high error
   rates.

2. Version pinning through NPM and Composer package managers is great for
   managing third party dependencies as long its not too many of them and they
   don't change too often. For internal dependencies its a lot of work to
   update dependencies between repositories all the time. Time gets lost by
   developers that don't have the correct dependencies or because of mistakes
   in the merge process.

3. Changing code in core libraries can break dependencies without the developer
   even realizing this because tests don't run together. This introduces a
   longer feedback cycle between code that depends on each other, with all the
   downsides.

One important remark about monolithic repositories: It does not automatically
lead to a monolithic code-base. Especially Symfony2 and ZF2 are a very
good example of how you can build individual components with a clean dependency
graph. 

At `Qafoo <http://qafoo.com>`_ we have always preferred monolithic project
repositories containing several components over many small independent ones. We
advised many customers to choose this approach except in some special cases
where going small was economically more efficient.

Benefits of Monlithic Repositories
----------------------------------

Even if you are not at the scale of Facebook or Google, a single repository
still provides the mentioned benefits:

- Adjusting to constant change by factoring out libraries, merging libraries
  and introducing new dependencies for multiple projects is much easier when
  done in a single, atomic VCS commit.

- Discoverability of code is much higher, if you have all the code in a single
  place. Github and Gitlab don't offer powerful tools like find, grep, sed over
  more than one repository. Hunting down dependencies, in specific versions can
  cost alot of time. 

- Reusability increases as it is much easier to just use code from the same
  repository than from another repository. Composer and NPM simplify combining
  repositories at specific versions, however one problem is actually knowing
  that the code exists in the first place.

- From an operational perspective it is much easier to get a new developer
  up to speed setting up projects from a single repository. Just practically
  its easier to add his public key to only one Team/Repository/Directory than
  to hundreds. On top of that setting up many small repositories and
  familiarizing with each of them costs a lot of time.

This is why I have been struggling with how Packagist and Satis force the move
to smaller repositories through the technical constraint "one repository equals
one composer.json file". For reusable open source projects this is perfectly
fine, but for company projects I have seen it hurt developer productivity more
often than is acceptable.

Introducing Fiddler
-------------------

So today I prototyped a build system that complements Composer to manage
multiple separate projects/packages in a single repository. I call it `Fiddler
<https://github.com/beberlei/fiddler>`_. Fiddler introduces a maintainable
approach to managing dependencies for multiple projects in a single repository,
without losing the benefits of having explicit dependencies for each separate
project.

In practice Fiddler allows you to manage all your third-party dependencies using a
``composer.json`` file, while adding a new way of managing your internal
dependencies. It combines both external and internal packages to a single
pool and allows you to pick them as dependencies for your projects.

For each project you add a ``fiddler.json`` file where you specify both your
third-party and internal dependencies. Fiddler will take care of generating a
specific autoloader for each project, containing only the dependencies of the
project.  This allows you to have one repository, while still having *explicit*
dependencies per project.

Keeping explicit dependencies for each project means it's still easy to find
out which components are affected by changes in internal or third-party
dependencies.

Example Project
---------------

Say you have three packages in your application, Library_1, Project_A
and Project_B and both projects depend on the library which in turn depends
on ``symfony/dependency-injection``. The repository has the following file structure:

::

    projects
    ├── components
    │   ├── Project_A
    │   │   └── fiddler.json
    │   ├── Project_B
    │   │   └── fiddler.json
    │   └── Library_1
    │       └── fiddler.json
    ├── composer.json

The ``fiddler.json`` of Library_1 looks like this:::

    {
        "autoload": {"psr-0": {"Library1\\": "src/"}},
        "deps": ["vendor/symfony/dependency-injection"]
    }

The ``fiddler.json`` of Project_A and Project_B look similar (except the autoload):::

    {
        "autoload": {"psr-0": {"ProjectA\\": "src/"}},
        "deps": ["components/Library_1"]
    }

The global ``composer.json`` as you would expect:::

    {
        "require": {
            "symfony/dependency-injection": "~2.6"
        }
    }

As you can see dependencies are specified without version constraints and as
directory paths relative to the project root. Since everything is in one
repository, all internal code is always versioned, tested and deployed
together. Dropping the need for explicit versions when specifying internal
dependencies.

With this setup you can now generate the autoloading files for each package
exactly like Composer would by calling::

    $ php fiddler.phar build
    Building fiddler.json projects.
     [Build] components/Library_1
     [Build] components/Project_A
     [Build] components/Project_B

Now in each package you can ``require "vendor/autoload.php";`` and it loads an
autoloader with all the dependencies specified for each component, for example
in ``components/Library_1/index.php``

.. code-block:: php

    <?php

    require_once "vendor/autoload.php";

    $container = new Symfony\Component\DependencyInjection\ContainerBuilder;

This is an early access preview, please test this, provide feedback if you see
this as a valuable or not and about possible extensions. See the `README
<https://github.com/beberlei/fiddler>`_ for more details about functionality
and implementation details.

The code is very rough and simple right now, you will probably stumble accross
some bugs, please `report them <https://github.com/beberlei/fiddler/issues>`_.
It is stable enough so that we could actually port `Tideways
<https://tideways.io>`_ to it already which is a multi package repository.

.. author:: default
.. categories:: PHP
.. tags:: Fiddler, BuildTools, Composer
.. comments::
