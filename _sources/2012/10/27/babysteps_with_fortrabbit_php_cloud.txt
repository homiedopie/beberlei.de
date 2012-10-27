Babysteps with Fortrabbit PHP Cloud
===================================

I wanted to host a simple application to play around with the `Tent Protocol
<https://tent.io>`_ (see `my last blogpost
<http://whitewashing.de/2012/10/22/a_tent_io_app__zelten_bookmarks.html>`_), so
I checked through some of the PHP Cloud providers again for the fun of it. One
requirement was to deploy from Git and update dependencies from Composer. I
found a new provider that i havent heard of before, `Fortrabbit
<https://www.fortrabbit.com/>`_ thats supports this so I had to check it out.
It has some more features that I really digg:

Fortrabbit provides you with a Git url where you can push your repository.
It is directly deployed during the push operation. You can trigger composer
updates by having a special syntax in the commit message. The push
output informs you about all the steps performed during deployment.

Addtionally you can configure environment variables in the web-administration
interface that are available in the application through ``$_SERVER``. You
can easily use them to configure your application, if its hosted in a public
repository. Great to share sample applications on Github and host them from
there.

You get SSH access to the machines, where you can take a look at the apache
and php error log files. You have vim available. Quite cool and very helpful
for any kind of debugging necessary. Deployments overwrite every change you
make, so its still a save environment.

The composer support allows for post install scripts, which is cool to perform
all sorts of cache warmup and other deployment tasks.

You can host one application for free, however they shutdown after 48 hours if
you don't regularly click on a reset button. Its definately enough to get small
prototypes up and running. From there you can upgrade in many small steps from
small plans (10€/month) to bigger ones (80€/month).

.. author:: default
.. categories:: none
.. tags:: none
.. comments::

