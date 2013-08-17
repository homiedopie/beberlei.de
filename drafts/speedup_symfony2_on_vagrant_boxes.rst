Speedup Symfony2 on Vagrant boxes
=================================

Using Symfony2 inside a Vagrant box is considered to be very slow (`here
<http://stackoverflow.com/questions/12161425/why-is-my-symfony-2-0-site-running-slowly-on-vagrant-with-linux-host>`_,
`here <https://twitter.com/spicy_sake/status/183135528567320576>`_), even when
using NFS. I can confirm the experience and know many others that reported the
same.

Without looking at an actual benchmark I always considered the problem to be
related to the huge number of files that a Symfony project normally ships with
and the I/O that is generated from ``filemtime`` calls to check if the
configuration files have changed.

This is true to some degree, but there are other bottlenecks that I have found
after finally doing some benchmarking with `XHProf
<https://github.com/facebook/xhprof>`_:

1. Monolog logs to the NFS share and the huge number ``fwrite`` take their toll.
2. Writing compiled Twig templates to the NFS share using ``file_put_contents``.
3. Assetic: Scanning for stylesheets and javascripts within templates is very
   slow, causing lots of I/O on the NFS share and CPU and changing it to using
   explicit bundling in the ``app/config/config.yml`` helps alot. You can use a
   cronjob deployed by Puppet/Chef that invokes the `assetic:dump` command with
   a `--watch` flag in the background.
4. JMSDiExtraBundle scans for Services to check for changes on service objects,
   causing considerable I/O.
5. ``ReplaceAliasWithActualDefinitionPass`` in Symfony DIC uses a set of
   recursive algorithms to replace aliases with the real services. That takes a
   huge amount of time in bigger applications including amounting calls to methods
   inside the pass over 100.000 times.

The slowest bottlenecks listed (1-4) are I/O bound, directly related to NFS.
The fix is simple, change the cache **AND** the log directory to
``sys_get_temp_dir()`` instead of writing to the NFS share. I actually tried
this before, but since I forgot the log directory, this felt like no difference
and I reverted the change.

Here is the code you should add to your ``AppKernel`` to give you a resonable
performance on a Vagrant box:

.. code-block:: php

    <?php

    class AppKernel extends Kernel
    {
        // ...

        public function getCacheDir()
        {
            if (in_array($this->environment, array('dev, 'test'))) {
                return sys_get_temp_dir() . '/appname/cache/' .  $this->environment;
            }

            return parent::getCacheDir();
        }

        public function getLogDir()
        {
            if (in_array($this->environment, array('dev, 'test'))) {
                return sys_get_temp_dir() . '/appname/logs';
            }

            return parent::getLogDir();
        }
    }

This brings the page rendering speeds down to between 1.5 and 3 seconds, which
is quite normal for the development environment even outside a virtual machine.

This tip obviously works for any kind of application that is heavy on I/O:
Don't perform this operations on the NFS share unless you wan't to suffer.

.. author:: default
.. categories:: PHP, Symfony
.. tags:: PHP, Symfony
.. comments::
