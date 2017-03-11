Speedup Symfony2 on Vagrant boxes
=================================

- **Update:** Added requirements to configure Vagrant and Virtualbox before
  trying my change.
- **Update 2:** Added link to Virtualbox Guest Additions plugin for Vagrant,
  thanks Peter Kruithof for the hint.

Using Symfony2 inside a Vagrant box is considered to be very slow (`here
<http://stackoverflow.com/questions/12161425/why-is-my-symfony-2-0-site-running-slowly-on-vagrant-with-linux-host>`_,
`here <https://twitter.com/spicy_sake/status/183135528567320576>`_), even when
using NFS. I can confirm the experience and know many others that reported the
same.

Before doing this changes make sure:

- You are using Vagrant 1.2 (not sure that makes a difference though)
- You are using NFS with Vagrant (`More
  <http://docs.vagrantup.com/v2/synced-folders/nfs.html>`_). If you are on
  Windows then this can already be the problem (Virtualbox FS is slow with
  Symfony, because of the large number of files.)
- You have the Vbox Guest Additions on the guest that match your system (`Vagrant Plugin <https://github.com/dotless-de/vagrant-vbguest>`_, `Manual Update <https://gist.github.com/fernandoaleman/5083680>`_)
- You have an opcode cache installed, either `apc` or `opcache`.
- You disable `xdebug` or `xhprof`.

Without looking at an actual benchmark (mistake!) I always considered the problem to be
related to the huge number of files that a Symfony project normally ships with
and the I/O that is generated from ``filemtime`` calls to check if the
configuration files have changed.

This is just a small part, there are other bottlenecks that I have found after
finally doing some benchmarking with `XHProf
<https://github.com/facebook/xhprof>`_, leading to a simple fix:

1. Monolog logs to the NFS share and the huge number ``fwrite`` take their toll.
2. Writing compiled Twig templates to the NFS share using ``file_put_contents``.
3. Assetic: Scanning for stylesheets and javascripts within templates is very
   slow, causing lots of I/O on the NFS share and CPU and changing it to using
   explicit bundling in the ``app/config/config.yml`` helps alot. You can use a
   cronjob deployed by Puppet/Chef that invokes the `assetic:dump` command with
   a `--watch` flag in the background.
4. JMSDiExtraBundle scans for Services to check for changes on service objects.
5. ``ReplaceAliasWithActualDefinitionPass`` in Symfony DIC uses a set of
   recursive algorithms to replace aliases with the real services. That takes a
   huge amount of time in bigger applications including amounting calls to methods
   inside the pass over 100.000 times.

The slowest bottlenecks listed (1-4) are I/O bound, directly related to NFS.
To fix this just change the cache **AND** the log directory to
``sys_get_temp_dir()`` or shared memory (/dev/shm) instead of writing to the
NFS share. I actually tried this before, but since I forgot the log directory,
this felt equally slow and I reverted the change.

Here is the code you should add to your ``AppKernel`` to give you a
considerable performance boost on a Vagrant box:

.. code-block:: php

    <?php

    class AppKernel extends Kernel
    {
        // ...

        public function getCacheDir()
        {
            if (in_array($this->environment, array('dev', 'test'))) {
                return '/dev/shm/appname/cache/' .  $this->environment;
            }

            return parent::getCacheDir();
        }

        public function getLogDir()
        {
            if (in_array($this->environment, array('dev', 'test'))) {
                return '/dev/shm/appname/logs';
            }

            return parent::getLogDir();
        }
    }

This brings the page rendering speeds down to between 0.5 and 1.5 seconds, which
is quite normal for the development environment even outside a virtual machine.

This tip obviously works for any kind of application that has a I/O intensive
development environment: Don't perform this operations on the NFS share unless
you wan't to suffer.

.. author:: default
.. categories:: PHP, Symfony
.. tags:: Vagrant, Symfony
.. comments::
