Monolithic Repositories with PHP and Composer
=============================================

As Git becomes more ubiquitous in open-source projects and within companies,
monolithic repositories containing multiple packages and repositories have
become a bit of a bad practice. This is a similar trend to how monolithic
applications are out of fashion and the recent focus on microservices and
Docker.

Yet just several years ago it was common that companies had just a single (or
few) SVN repository and within it contained the code for all the projects.  One
open source example of this even today is the `SVN repository
<http://svn.apache.org/repos/asf/>`_ of the Apache Software Foundation with a
breath taking number of 1.672.730 commits across many of their projects.

However recently the move towards smaller repositories is questioned by three
extremely productive organizations at incredible scale (compared to the usual
PHP shop) speaking about their use of monolithic repositories.

Facebook `mentioned on their F8 2015 conference
<https://developers.facebooklive.com/videos/561/big-code-developer-infrastructure-at-facebook-s-scale>`_
that they are going to merge their three big code repositories Server, iOS and
Android into a single big repository over the course of 2015. A dedicated team
working on Mercurial at Facebook made this possible and even increase the
performance.

Google open-sourced `Bazel <http://bazel.io>`_, the build tool behind a huge
chunk of their codebase out of a single Perforce repository with over 20 million
commits (`Reference
<http://www.perforce.com/sites/default/files/still-all-one-server-perforce-scale-google-wp.pdf>`).

Twitter has open-sourced their clone of Google's Bazels build system a little
longer: `Pants <https://pantsbuild.github.io/>`_ is also designed for
monolithic repositories.

All three companies cite huge developer productivity benefits,
code-reusability, large-scale refactorings and development at scale for
choosing this approach. The Facebook talk even mentions how all their
development infrastructure efforts focus on keeping this workflow because of
the benefits it brings.

In contrast working with ever smaller repositories can be a huge burden for
developer mental models: I have seen this in open-source projects such as
Doctrine and many customer projects as well as our own product Tideways:

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

Take for example Doctrine, which was managed in a single Git repository until
the late 2.0 Beta, then split into Common, DBAL and ORM and later split into
even smaller packages by splitting Common. This was only possible because
Composer exists.

However in my opinion since the splits the visibility of Pull Requests and
problems in smaller components has suffered a lot. Each Common subproject now
has its own versioning numbers, confusing even seasoned contributors on which
versions are compatible with each other. 

Symfony2 and ZendFramework2 have rejected this split into smaller packages.
Both frameworks have a lot of independent and reusable components, but are
still managed from one central repository. Technical tools are used to make
each component usable on its own from Composer/Packagist. Given my experience
from Doctrine I am glad they didn't.

At `Qafoo <http://qafoo.com>` we have always preferred monolithic project
repositories over many small independent ones and advised many customers to
choose this approach except in some special cases where going small was
economically more efficient.

Even if you are not at the scale of Facebook or Google, a single repository
still provides their mentioned benefits:

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
  to hundrets. On top of that setting up many small repositories and
  familiarizing with each of them costs a lot of time.

This is why I have been struggling with how Composer forces the move to smaller
repositories through the technical constraint "one repository equals one
composer.json file". For reusable open source project with few dependencies
this is perfectly fine, but for company projects I have seen it hurt developer
productivity more often than is acceptable.

So today I took some time to work on a prototype build system that integrates
Composer with multiple packages in a single large repository.

I call it `Fiddler <https://github.com/beberlei/fiddler>`_. It allows you to define
lightweight packages inside one big repository by adding ``fiddler.json`` files
to each package directory. Fiddler packages can depend on each other or on
third party packages defined in a single global ``composer.json`` in the
project root. The ``fiddler.json`` also defines the autoload rules for each
package.

Say you have three packages in your application, Foo, Bar and Baz and both Bar
and Baz depend on Foo, and Foo depends on ``symfony/dependency-injection`` with
the following file structure:

::

    projects
    ├── components
    │   ├── bar
    │   │   └── fiddler.json
    │   ├── baz
    │   │   └── fiddler.json
    │   └── foo
    │       └── fiddler.json
    ├── composer.json

The ``fiddler.json`` of Foo looks like this:::

    {
        "autoload": {"psr-0": {"Foo\\": "src/"}},
        "deps": ["vendor/symfony/dependency-injection"]
    }

The ``fiddler.json`` of Bar and Baz look similar (except the autoload):::

    {
        "autoload": {"psr-0": {"Bar\\": "src/"}},
        "deps": ["components/foo"]
    }

As you can see dependencies are specified without version constraints and as
directory paths relative to the project root. As the repository can only be at
a single revision at the same time, every package it at the same version. This
makes version constraints superfluous.

With this setup you can now generate the autoloading files for each package
exactly like Composer would by calling::

    $ php fiddler.phar build

Now in each package Foo, Bar and Baz you can ``require "vendor/autoload.php";``
and it loads an autoloader with all the dependencies specified for each
component, for example in ``components/foo/index.php``::

    <?php

    require_once "vendor/autoload.php";

    $container = new Symfony\Component\DependencyInjection\ContainerBuilder;

This is an early access preview, please test this, provide feedback if you see
this as a valuable or not and about possible extensions. See the `README
<https://github.com/beberlei/fiddler>`_ for more details about functionality
and implementation details.

The code is very rough and simple right now, you will probably stumble accross
some bugs. It is stable enough so that we could actually port `Tideways
<https://tideways.io>`_ to it already which is a multi package repository.

.. author:: default
.. categories:: PHP
.. tags:: Fiddler, BuildTools, Composer
.. comments::
