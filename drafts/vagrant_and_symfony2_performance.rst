Vagrant and Symfony2 Performance
================================

Using Symfony2 inside a Vagrant box is considered to be very slow (`here
<http://stackoverflow.com/questions/12161425/why-is-my-symfony-2-0-site-running-slowly-on-vagrant-with-linux-host>`_,
`here <https://twitter.com/spicy_sake/status/183135528567320576>`_), even when
using NFS. I can confirm the experience and know many others that reported the
same.

Without looking at an actual benchmark I always considered the problem to be
related to the huge number of files that a Symfony project normally ships with
and the I/O that is generated from ``filemtime`` calls to check if the
configuration files have changed. ``filemtime`` is really the performance
killer for NFS.

This is true to some degree, but there are other bottlenecks that I have found
while doing some benchmarking with Xprof:

1. Monolog logs to the NFS share, takes about 7 seconds to ``fwrite`` for 800
   messages.
2. JMSDiExtraBundle scans for Services, takes about 1-2 Seconds on a large
   application to check for changes on service objects.
3. ``ReplaceAliasWithActualDefinitionPass`` in Symfony DIC uses a set of
   recursive algorithms to replace aliases with the real services. That takes a
   huge amount of time in my application, including amounting calls to methods
   inside the pass over 100.000 times.
4. Writing compiled Twig templates to disc using file_put_contents, takes about
   44 seconds for 2300 template files on `cache:clear` including the warmup.

The fix is simple, change the cache AND the log directory to
``sys_get_temp_dir()`` instead of writing to the NFS disk. I actually tried
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

.. author:: default
.. categories:: PHP, Symfony
.. tags:: PHP, Symfony
.. comments::
