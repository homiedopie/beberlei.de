Babysteps with Fortrabbit PHP Cloud
===================================

To host a simple application I wanted to check through some of the PHP Cloud
providers again. One requirement was to deploy from Git and update dependencies
from Composer. Apparently no PHP cloud I found supported Composer yet except
this rather new one called `Fortrabbit <https://www.fortrabbit.com/>`_.
It has some more features that I really digg:

Fortrabbit provides you with a Git url where you can push your repository.
It is directly deployed during the push operation. You can trigger composer
updates by having a special syntax in the commit message. The push
output informs you about all the steps performed during deployment.

Addtionally you can configure environment variables in the web-administration
interface that are available in the application through ``$_SERVER``. You
can easily use them to configure your application, if its hosted in a public
repository.

You get SSH access to the machines, where you can take a look at the apache
and php error log files. You have vim available. Quite cool and very helpful
for any kind of debugging necessary. Deployments overwrite every change you
make, so its still a save environment.

You can host 3 applications for free, however they shutdown after 48 hours if
you don't regularly click on a reset button. Its definately enough to get small
prototypes up and running. From there you can upgrade in many small steps from
small plans (10€/month) to bigger ones (80€/month).

.. author:: default
.. categories:: none
.. tags:: none
.. comments::

