Resources for a PHP and Hudson CI Integration
=============================================

Yesterday I finally had the time to setup my first continuous
integration environment. Possible solutions for CI are
`phpUnderControl <http://phpundercontrol.org/about.html>`_,
`Hudson <http://www.hudson-ci.org>`_ or
`Arbit <http://www.arbitracker.org>`_. Although phpUnderControl is the
most wide-spread, but from I heard complex to setup/maintain, solution
[STRIKEOUT:supposedly a hack] and Arbit just in an early Alpha I decided
to give Hudson a shoot. Another reason for this decision, I heard it has
a simple plugin architecture and is easy to install and use.
Additionally Hudson is easily integrated into
`Netbeans <http://www.netbeans.org>`_ and
`Redmine <http://www.redmine.org>`_, and I use both tools regularly in
development.

My motivation to dive into CI is easily explained. I just never felt it
was necessary to add a continuous integration environment to my projects,
since I had one or two simple bash scripts that did the job. In general
this is rather annoying, because they mostly only run PHPUnit and have
to be done using a cronjob or manually, without any real process of
notification. Additionally you have no way to navigate the test-results,
code-coverage and no history of the last builds. For projects like
`Doctrine 2 <http://www.doctrine-project.org>`_ we have the additional
requirement to support 4 different database platforms, i.e. 4 different
PHPUnit configurations. Currently that is solved by me using a Bash
script that iterates over the configuration file names and invokes
PHPUnit.

There are already some awesome sources how to get Hudson and PHP
working. I'll list them here:

-  `Sebastian Bergmann's Howto in
   Screenshots <http://www.flickr.com/photos/sebastian_bergmann/sets/72157622541690849/>`_
-  `David Luhman's series on PHP and
   Hudson <http://luhman.org/blog/2009/12/16/installing-hudson-phing-phpunit-and-git-ubuntu>`_
-  `Justin Palmers Guide to install PHP and Hudson (With
   Screenshots) <http://blog.jepamedia.org/2009/10/28/continuous-integration-for-php-with-hudson/>`_

All those guides are already awesome and I would recommend choosing one
of those to install Hudson, I think i can't add anything new to those. I
have used Sebastians Howto, however i also like the third one. David
Luhmans guide adds lots of details that are important to get the
different parts of a build process to work.

Now what these tutorials all do is that they use a bash command to
execute the build process or specify an Ant Build file. However there
is also a Phing Build process plugin for Hudson that allows to specify
the build.xml targets to execute in the process. From the "Available
Plugins" list you can choose the "Phing plugin".

After installation you have to configure the Phing install. The `Phing
Plugin Wiki
Page <http://wiki.hudson-ci.org/display/HUDSON/Phing+Plugin>`_ shows how
to do this. You have to go to "Manage Hudson" => "Configure System" and
look for Phing. There you find the dialog to configure your phing
installations.

In the context of choosing a build script for your project you can now
choose "Phing" instead of Ant:

.. figure:: http://www.flickr.com/photos/sebastian_bergmann/4046549930/in/set-72157622541690849/
   :align: center
   :alt: 
You can enter the targets to build, for example on my local Hudson
instance I only execute "test" for Doctrine 2, since I am not interested
in the building and deployment onto the PEAR channel at this development
stage.

From inside Netbeans you can then start builds by pointing to the Hudson
instance. See this tutorial by one of the `Hudson + Netbeans
Developers <http://blogs.sun.com/joshis/entry/hudson_integration_in_netbeans_6>`_.
You can then start all the builds from inside Netbeans and be notified
of the success or failure.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>