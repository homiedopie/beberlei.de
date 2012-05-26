Trying a Two Step PEAR/PHAR approach to develop and deploy
==========================================================

With PHP 5.3 the PHAR extension is a pretty powerful concept for all
your deployment needs, however it does not tell the complete story.
Frameworks, Libraries and many different of them are used throughout
applications and in recent times people even began to chery-pick the
best components from each of the frameworks and package them together.
With Pirum being a simple PEAR channel server there is also momentum for
projects to distribute their code via PEAR.

However PEAR is mostly used in the server-wide configuration use-case,
which is not very useful if you plan to distribute your complete
application in one PHAR file. I just recently had the idea for this
scenario, so please bear with me and add all the feedback and comments
you can come up with. I tested this with the ongoing rewrite of my blog
software.

First we'll add a new user that we develop our application with:

::

    sudo useradd -m -g www-data whitewashing
    sudo passwd whitewashing
    su - whitewashing

Now there is the possibility that with this user PHP and PEAR is not in
your $PATH enviroment, so you might have to add it. In my case on Ubuntu
i also had to switch the console from /bin/sh to /bin/bash for this
user. Then we need to setup our application, I am going to use the Zend
Framework project style here but with a little twist. We will add a
distinction between vendor and project libraries by adding a *vendor*
directory into the main folder.

But first we create a folder for our application, and create a Zend
Framework project in the subfolder "trunk", which will be the focus of
our development.

::

    whitewashing@desktop:~$ mkdir whitewashing
    whitewashing@desktop:~$ zf create project whitewashing/trunk
    Creating project at /home/whitewashing/whitewashing/trunk
    whitewashing@desktop:~$ mkdir whitewashing/trunk/vendor

Now we can configure an Apache virtual host to point to our
/home/whitewashing/whitewashing/public directory, i call this
"whitewashing-dev" add it to my /etc/hosts and can visit the dummy
project page.

We then configure our PEAR installation for the specific application
user and re-configure the bin and php library paths:

::

    whitewashing@desktop:~$ pear create-config /home/whitewashing/ .pearrc
    whitewashing@desktop:~$ pear config-set php_dir /home/whitewashing/whitewashing/trunk/vendor
    whitewashing@desktop:~$ pear config-set bin_dir /home/whitewashing/whitewashing/trunk/bin

This configuration assumes that we will install all our stuff into our
development trunk. From there also the PEAR installed libraries might be
copied into branches or tags. PEAR Project tests, configuration and
web-files will still be put by default under $HOME/pear/\*. We don't
need them for our applications.

Now we install all the dependencies our project needs, in this case Zend
Framework, Doctrine 2, HTML Purifier:

::

    whitewashing@desktop:~$ pear channel-discover pear.zfcampus.org
    whitewashing@desktop:~$ pear install zfcampus/zf-alpha
    whitewashing@desktop:~$ pear channel-discover htmlpurifier.org
    whitewashing@desktop:~$ pear install hp/HTMLPurifier
    whitewashing@desktop:~$ pear channel-discover pear.phpdoctrine.org
    whitewashing@desktop:~$ pear install pear.phpdoctrine.org/DoctrineORM-2.0.0

Now we have all three of the packages installed in our project folder
*whitewashing/trunk/vendor*, see:

::

    whitewashing@desktop:~$ ls -aFl whitewashing/trunk/vendor/
    total 680
    drwxr-xr-x  7 whitewashing www-data   4096 2009-12-13 14:45 ./
    drwxr-xr-x  8 whitewashing www-data   4096 2009-12-13 14:36 ../
    drwxr-xr-x  3 whitewashing www-data   4096 2009-12-13 14:43 .channels/
    -rw-r--r--  1 whitewashing www-data     57 2009-12-13 14:45 .depdb
    -rw-r--r--  1 whitewashing www-data      0 2009-12-13 14:45 .depdblock
    drwxr-xr-x  5 whitewashing www-data   4096 2009-12-13 14:45 Doctrine/
    -rw-r--r--  1 whitewashing www-data 582208 2009-12-13 14:45 .filemap
    drwxr-xr-x 20 whitewashing www-data   4096 2009-12-13 14:39 HTMLPurifier/
    -rw-r--r--  1 whitewashing www-data    629 2009-12-13 14:39 HTMLPurifier.autoload.php
    -rw-r--r--  1 whitewashing www-data    274 2009-12-13 14:39 HTMLPurifier.auto.php
    -rw-r--r--  1 whitewashing www-data    545 2009-12-13 14:39 HTMLPurifier.func.php
    -rw-r--r--  1 whitewashing www-data   9299 2009-12-13 14:39 HTMLPurifier.includes.php
    -rw-r--r--  1 whitewashing www-data    955 2009-12-13 14:39 HTMLPurifier.kses.php
    -rw-r--r--  1 whitewashing www-data   8831 2009-12-13 14:39 HTMLPurifier.php
    -rw-r--r--  1 whitewashing www-data  11901 2009-12-13 14:39 HTMLPurifier.safe-includes.php
    -rw-r--r--  1 whitewashing www-data      0 2009-12-13 14:45 .lock
    drwxr-xr-x  8 whitewashing www-data   4096 2009-12-13 14:43 .registry/
    drwxr-xr-x 59 whitewashing www-data   4096 2009-12-13 14:36 Zend/
    -rw-r--r--  1 whitewashing www-data  19537 2009-12-13 14:36 zf.php

And both Doctrine and ZF registered their binary CLi tools inside the
*whitewashing/trunk/bin/*folder:

::

    whitewashing@desktop:~$ ls -aFl bin/
    total 20
    drwxr-xr-x 2 whitewashing www-data 4096 2009-12-13 14:45 ./
    drwxr-xr-x 8 whitewashing www-data 4096 2009-12-13 14:36 ../
    -rwxr-xr-x 1 whitewashing www-data   50 2009-12-13 14:45 doctrine*
    -rwxr-xr-x 1 whitewashing www-data  169 2009-12-13 14:45 doctrine.php*
    -rwxr-xr-x 1 whitewashing www-data 1511 2009-12-13 14:36 zf*

We now have the full control over the versions of our dependencies, we
can call "pear upgrade " whenever we want to update one of the ZF,
Doctrine or HtmlPurifier libraries inside our application.

Now some magic is gonna happen, we start to develop our application and
such which is all not really interesting for this topic. At some point
we want to package it all up into a PHAR file and distribute it. We want
to package our application in one big phar file. We also want to make
sure that the configuration files in
*whitewashing/trunk/application/configs/* are not distributed, but have
to be created on the server and are kept that way. We could write an
installer script for this configuration management.

The reference for PHAR files is the PHP Manual for the Basics and Cal
Evans' two posts
(`1 <http://blog.calevans.com/2009/07/19/lessons-in-phar/>`_,
`2 <http://blog.calevans.com/2009/07/26/packaging-zend-framework-as-a-phar-revisited/>`_)
on this topic, aswell as `a post on
Geekmonkey <http://geekmonkey.org/articles/PHP_Archives>`_. Contrary to
most other PHP extensions, PHAR has an extensive documentation, however
its not organized terribly well. Also there are no real use-cases and
scenarios discussed, methods are only looked at in isolation. Cals posts
are very good on understanding how to package up different libraries,
but there is no word on distributing web applications. That is where the
Geekmonkey post comes in to wire it all together.

For a Zend Framework application that should have both a web and a cli
(cronjobs) entry point into the application we need a specific stub file
for the PHAR bootstrapping. A stub is a little PHP script that is
executed whenever your PHAR file is included into your php script. It is
essentially a front-controller for your PHAR application. It also has
mount capabilities that allow to import files or directories from
outside into the PHAR context. This is a powerful feature that is
required to distribute configurable applications like our blog.

This screenshot shows how the application is currently structued in
development mode. In production its structure should look like:

::

    whitewashing
    |--application
    |  |--configs
    |     |-- my application config files are all here...
    |--bin
    |  |--whitewashing.php
    |--public
    |  |--index.php
    |  |--.htaccess
    |--whitewashing.phar

The whitewashing.php and index.php files are the application entry
points that only include the phar file and trigger the application
bootstrapping that will be included in the Stub file. They both look
like:

::

    <?php
    define('EXTERNAL_APPLICATION_ROOT', __DIR__."/../");
    include EXTERNAL_APPLICATION_ROOT."/whitewashing.phar";

Including a PHAR file essentially has two conesequences:

-  The PHAR path will be added to your include path.
-  The stub file will be executed.

Our application stub looks like this:

::

    <?php

    if(defined('EXTERNAL_APPLICATION_ROOT')) {
        // Mount the external application/configs directory as config if it exists.
        if (file_exists(EXTERNAL_APPLICATION_ROOT."/application/configs")) {
            Phar::mount("application/configs", EXTERNAL_APPLICATION_ROOT."/application/configs");
        }
    }

    /** Zend_Loader_Autoloader */
    require_once 'Zend/Loader/Autoloader.php';
    $autoloader = Zend_Loader_Autoloader::getInstance();

    if (php_sapi_name() == "cli") {
        require_once 'bin/whitewashing.php';
    } else {
        require_once 'public/index.php';
    }

    __HALT_COMPILER();

The first bit of the stub mounts the external application configs
directory into the stub and hides possible directories that are present
at this location in the PHAR file. This allows us to distribute our
application with a default configuration, but allows any user to replace
the configuration files to fit the application to his need.

The second bit loads Zend Framework Autoloader that is required by the
bootstrapping mechanism. The third bit decides wheater this request is
executed from the CLI- or the Web-Entry point of the application. The
fourth bit, ``__HALT_COMPILER();`` is a technically required call inside
your stub-file.

Now that we have a stub-file for our application, we can package it and
distribute it. I am using a modified version of Cal Evans example for
this. I have extracted his directory traversal to find all the relevant
into a re-usable FilterIterator implementation. I `pasted my package.php
a Gist <https://gist.github.com/3b20264b857dbdabf526>`_ on Github. Now
this should probably be put into the build context of your application,
possibly as a phing or ant task or something alike.

Now what this build process does not manage is the creation of the
application entry point php and .htaccess files, but since they won't
ever change its easy to add them to the build directory for now. An even
more sophisiticated version of the build script would lead to the
creation of an additional tar.gz of the complete application folder. Our
deployment process would then be as easy as:

-  If the application is not installed yet, unpack the tarball into its
   location.
-  If the application should be updated, just replace the PHAR file.

If you need the ability to go back to any version of your application
you could make use of symlinks.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>