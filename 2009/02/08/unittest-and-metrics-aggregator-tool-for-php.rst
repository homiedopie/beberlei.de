Unittest and Metrics Aggregator Tool for PHP
============================================

Both `PHPUnit <http://www.phpunit.de>`_ and
`PDepend <http:/www.pdepend.org>`_ offer export functionality in XML or
in a Test-database that is not quite readable for any user from the
start. Over the last month I have gradually written `a nice webbased
tool <http://wiki.github.com/beberlei/puma>`_, that aggregates this data
and (todo in the future) relates them to help me with my open source
projects.

PHPUnit can be used with a **--test-db-dsn** command, which saves all
information about tests into a Database and PDepend has a strong Package
centric source parser for all sorts of project metrics.

What I needed for my `Zend Framework <http://framework.zend.com>`_
related work (and other projects) was a tool that does a run of the
complete test-suite for me and saves the information, so that I can see
where problems occur (and if they are due to my changes or other
peoples). Since PHPUnit will stopped calculating additional metrics, I
have also integrated the fabulous PDepend Tool into this aggregator. It
shows me, what classes and functions need refactoring due to complexity
issues and draws some nice graphs that summarize all sorts of project
related information on a per package basis.

You can `download or clone the an alpha version at
Github <http://wiki.github.com/beberlei/puma>`_. Its written with
`ezcMvcTools <http://www.ezcomponents.org>`_, so you need this to work
too. A list of `some screenshots is at the Github Wiki
page <http://wiki.github.com/beberlei/puma>`_.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>