How I use Wordpress with Git and Composer
=========================================

I maintain two Wordpress blogs for my wife and wanted to find a workflow to
develop, update, version-contol and maintain them with Git and Composer, like I
am used to with everything else that I am working on. 

The resulting process is a combination of several blog posts and my own
additions, worthy of writing about for the next person interested in this
topic.

It turns out this is quite simple if you re-arrange the Wordpress directory
layout a little bit and use some fantastic open-source projects to combine
Wordpress and Composer.

Initialize Repository
---------------------

As a first step, create a new directory and git repository for your blog:

::

    $ mkdir myblog
    $ cd myblog
    $ git init

Create a docroot directory that is publicly available for the webserver:

::

    $ mkdir htdocs

Place the index.php file in it that delegates to Wordpress (installed later):

.. code-block:: php

    <?php
    // htdocs/index.php
    // Front to the WordPress application. This file doesn't do anything, but loads
    // wp-blog-header.php which does and tells WordPress to load the theme.

    define('WP_USE_THEMES', true);
    require( dirname( __FILE__ ) . '/wordpress/wp-blog-header.php' );

Create the wp-content directory inside the docroot, it will be configured to
live *outside* the Wordpress installation.

::

    $ mkdir htdocs/wp-content -p

And then create a `.gitignore` file with the following ignore paths:

    /htdocs/wordpress/
    /htdocs/wp-content/uploads
    /htdocs/wp-content/plugins
    /htdocs/wp-content/themes

If you want to add a custom theme or plugin you need to use `git add -f` to
force the ignored path into Git.

Don't forget to include the uploads directory in your backup, when deploying
this blog to production.

You directory tree should now look like this:

::

    .
    ├── .git
    ├── .gitignore
    └── htdocs
        ├── index.php
        └── wp-content

In the next step we will use Composer to install Wordpress and plugins.

Setup Composer
--------------

Several people have done amazing work to make Wordpress and all the plugins and
themes on Wordpress.org available through Composer. To utilize this work we
create a composer.json file inside our repository root. There the file is
outside of the webservers reach, users of your blog cannot download the
composer.json.

::

    {
        "require": {
            "ext-gd": "*",
            "wpackagist-plugin/easy-media-gallery": "1.3.*",
            "johnpbloch/wordpress-core-installer": "^0.2.1",
            "johnpbloch/wordpress": "^4.4"
        },
        "extra": {
            "installer-paths": {
                "htdocs/wp-content/plugins/{$name}/": ["type:wordpress-plugin"],
                "htdocs/wp-content/themes/{$name}/": ["type:wordpress-theme"]
            },
            "wordpress-install-dir": "htdocs/wordpress"
        },
        "repositories": [
            {
                "type": "composer",
                "url": "http://wpackagist.org"
            }
        ]
    }

This Composer.json is using the execellent `Wordpress Core Installer
<https://github.com/johnpbloch/wordpress-core-installer>`_ by `John P. Bloch
<https://johnpbloch.com/>`_ and the `WPackagist <http://wpackagist.org/>`_
project by `Outlandish <http://outlandish.com/>`_.

The ``extra`` configuration in the file configures Composer for placing
Wordpress Core and all plugins in the correct directories. As you can see we
put core into `htdocs/wordpress` and plugins into `htdocs/wp-content/plugins`.

Now run the Composer install command to see the intallation output similar
to the next excerpt:

::

    $ composer install
    Loading composer repositories with package information
    Installing dependencies (including require-dev)
      - Installing composer/installers (v1.0.23)
        Loading from cache

      - Installing johnpbloch/wordpress-core-installer (0.2.1)
        Loading from cache

      - Installing wpackagist-plugin/easy-media-gallery (1.3.93)
        Loading from cache

      - Installing johnpbloch/wordpress (4.4.2)
        Loading from cache

    Writing lock file
    Generating autoload files

The next step is to get Wordpress running using the Setup Wizard.

Setup Wordpress
---------------

Follow the Wordpress documentation to setup your Wordpress blog now, it
will create the neccessary database tables and give you `wp-config.php` file
to download. Copy this file to `htdocs/wp-config.php` and modify it slightly,
it is necessary to adjust the ``WP_CONTENT_DIR``, ``WP_CONTENT_URL`` and
``ABSPATH`` constants:

.. code-block:: php

    <?php

    // generated contents of wp-config.php, salts, database and so on

    define('WP_CONTENT_DIR',    __DIR__ . '/wp-content');
    define('WP_CONTENT_URL',    WP_HOME . '/wp-content');

    /** Absolute path to the WordPress directory. */
    if ( !defined('ABSPATH') ) {
        define('ABSPATH', dirname(__FILE__) . '/wordpress');
    }

    /** Sets up WordPress vars and included files. */
    require_once(ABSPATH . 'wp-settings.php');

Voila. You have Wordpress running from a Git repository and maintain
the Wordpress Core and Plugins through Composer.

Different Development and Production Environments
-------------------------------------------------

The next step is introducing different environments, to allow using
the same codebase in production and development, where the base urls are
different, without having to change ``wp-config.php`` or the database.

Wordpress relies on the 
``SITEURL`` and ``HOME`` configuration variables from the
``wp_options`` database table by default, this means its not easily possible to
use the blog under ``http://myblog.local`` (development) and
`https://myblog.com`` (production).

But working on the blog I want to copy the database from production and have
this running on my local development machine without anything more than
exporting and importing a MySQL dump.

Luckily there is an easy workaround that allows this: You can overwrite the
``SITEURL`` and ``HOME`` variables using constants in ``wp-config.php``.

For development I rely on the built-in PHP Webserver that is available since
PHP 5.4 with a custom router-script (I found this on a blog a long time ago,
but cannot find the source anymore):

.. code-block:: php

    <?php
    //htdocs/router.php

    $root = $_SERVER['DOCUMENT_ROOT'];
    chdir($root);
    $path = '/'.ltrim(parse_url($_SERVER['REQUEST_URI'])['path'],'/');
    set_include_path(get_include_path().':'.__DIR__);

    if(file_exists($root.$path)) {
        if(is_dir($root.$path) && substr($path,strlen($path) - 1, 1) !== '/') {
            $path = rtrim($path,'/').'/index.php';
        }

        if(strpos($path,'.php') === false) {
            return false;
        } else {
            chdir(dirname($root.$path));
            require_once $root.$path;
        }
    } else {
        include_once 'index.php';
    }

To make your blog run flawlessly on your dev machine, open up
``htdocs/wp-config.php`` and add the following if statement to rewrite
``SITEURL`` and ``HOME`` config variables:

.. code-block:: php

    <?php
    // htdocs/wp-config.php

    // ... salts, DB user, password etc.

    if (php_sapi_name() === 'cli-server' || php_sapi_name() === 'srv') {
        define('WP_ENV',        'development');
        define('WP_SITEURL',    'http://localhost:8000/wordpress');
        define('WP_HOME',       'http://localhost:8000');
    } else {
        define('WP_ENV',        'production');
        define('WP_SITEURL',    'http://' . $_SERVER['SERVER_NAME'] . '/wordpress');
        define('WP_HOME',       'http://' . $_SERVER['SERVER_NAME']);
    }

    define('WP_DEBUG', WP_ENV === 'development');

You can now run your Wordpress blog locally using the following command-line
arguments:

::

    $ php -S localhost:8000 -t htdocs/ htdocs/router.php

Keep this command running and visit `localhost:8000`.

.. author:: default
.. categories:: none
.. tags:: Wordpress
.. comments::
