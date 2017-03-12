Composer Monorepo Plugin (previously called Fiddler)
====================================================

I have `written about monorepos
<http://www.whitewashing.de/2015/04/11/monolithic_repositories_with_php_and_composer.html>`_
in this blog before, `presented a talk
<https://qafoo.com/resources/presentations/symfony_live_berlin_2015/monorepos.html>`_
about this topic and released a standalone tool called "Fiddler" that helps
integrating Composer with a monolithic repository.

At the beginning of the year, somebody in ``#composer-dev`` IRC channel on
Freenode pointed me in the direction of Composer plugins to use with Fiddler
and it was an easy change to do so.

With the help of a new Composer v1.1 feature to add custom commands from a
plugin, Fiddler is now "gone" and I renamed the repository to the practical
**beberlei/composer-monorepo-plugin** package name on `Github
<https://github.com/beberlei/composer-monorepo-plugin>`_. After you install
this plugin, you have the possibility to maintain subpackages and their
dependencies in a single repository.

::

    $ composer require beberlei/composer-monorepo-plugin

To use the plugin add **monorepo.json** files into each directory of a
subpackage and use a format similar to the **composer.json** to add
dependencies to a.) external composer packages that you have listed in your
global Composer file b.) other subpackages in the current monorepo.
See this example for a demonstration:

::

    {
        "deps": [
            "vendor/symfony/http-foundation",
            "components/Foo"
        ],
        "autoload": {
            "psr-0": {"Bar": "src/"}
        }
    }

This subpackage here defined in a hypothetical file
**components/Bar/monorepo.json** has dependencies to Symfony HTTP foundation
and another subpackage Foo with its own **components/Foo/monnorepo.json**.
Notice how we don't need to specify versions (they are implicit) and import
other dependencies using the relative path from the global composer.json.

The monorepo plugin is integrated with Composer, so every time you perform install,
update or dump-autoload commands, the subpackages will be updated as well and
each get their own autoloader that can be included from ``vendor/autoload.php``
relative to the subpackages root directory as usual.


.. author:: default
.. categories:: none
.. tags:: Monorepos, Composer
.. comments::
