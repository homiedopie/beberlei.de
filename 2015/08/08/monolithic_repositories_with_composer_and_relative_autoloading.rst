Monolithic Repositories with Composer and Relative Autoloading
==============================================================

Just was `reminded on Twitter by Samuel
<https://twitter.com/samuelroze/status/630037676654206976>`_ that there
is a way for monolithic PHP repositories with multiple components
that I haven't mentioned in my `previous post
<http://www.whitewashing.de/2015/04/11/monolithic_repositories_with_php_and_composer.html>`_.

It relies on a new composer.json for each component and uses
the autoloading capabilities of Composer in a hackish way.

Assume we have two components located in ``components/foo`` and
``components/bar``, then if bar depends on foo, it could define
its ``components/bar/composer.json`` file as:

::

    {
        "autoload": {
            "psr-0": {
                "Foo": "../foo/src/"
            }
        }
    }

This approach is very simple to start with, however it has some downsides
you must take into account:

- you have to redefine dependencies in every composer.json that relies
  on another component.

- if foo and bar depend on different versions of some third library ``baz``
  that are not compatible, then composer will not realize this and your
  code will break at runtime.

- if you want to generate deployable units (tarballs, debs, ..) then
  you will have a hard time to collect all the implicit dependencies
  by traversing the autoloader for relative definitions.

- A full checkout has multiple vendor directories with a lot of duplicated
  code.

I think this approach is ok, if you are only sharing a small number of
components that don't define their own dependencies. The `Fiddler
<https://github.com/beberlei/fiddler>`_ approach however solves all these
problems by forcing to rely on the same dependencies in a project globally and
only once.

.. author:: default
.. categories:: none
.. tags:: Monorepos
.. comments::
