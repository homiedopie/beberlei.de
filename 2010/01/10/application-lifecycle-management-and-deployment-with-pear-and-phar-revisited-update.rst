.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Application Lifecycle Management and Deployment with PEAR and PHAR (revisited) *UPDATE*
=======================================================================================

Some weeks ago `I posted an
article <http://www.whitewashing.de/blog/articles/123>`_ on using PEAR
and PHAR for application lifecycle management and deployment. Since then
I have gotten some feedback through comments, but also discussed the
topic with collegues. I have also optimized the approach quite
considerably and even `made an open-source project out of parts of
it <http://github.com/beberlei/pearanha>`_ and I want to share all that
is new with you. First of all, yes the presented solution was somewhat
complex, partly because it is still a proposed idea and definately up
for optimizations. However I am still very convinced of my approach,
something I should discuss in more detail.

The only other two languages I have ever programmed something in with
more than 50 lines of code are Java and C#. In both languages you can
explicitly import different dependencies like libraries and frameworks
by adding them to your application, i.e. in java you would add for
example Spring as an MVC Web layer, Hibernate as an ORM and several
other things to your project and directly bundle them in your
executable. This is very easy to configure and maintain in IDEs like
Netbeans or Eclipse (C# has the same with allowing you to attach DDLs of
libraries to your project). It also makes for a much more
straightforward deployment.

In the PHP world this siutation was quite different (up to PHP 5.3) for
several reasons:

-  You could not package a library into a single distributable file.
-  The PEAR installer as the only tool for updating and managing
   dependencies of your application by default installs into a
   system/global directory. This means dependencies your application
   uses are located in a completly different location than your
   application code.
-  You can't manage multiple versions of the same package with PEAR in
   this system directory, making it very hard to control servers with
   different applications.
-  The global directory with your application dependencies is most often
   not under version control, which makes deployment of applications
   with PEAR dependencies somewhat difficult.

There are some solutions to this problems:

-  Don't use PEAR, but put all dependencies in your version control
   system.
-  Don't use PEAR, and bundle dependencies to your code in the
   build/deployment process.
-  Use PEAR like in the article described, on a per project basis.

The solutions that don't use PEAR suffer from the disadvantage that you
need to keep track of all the library and framework dependencies
yourself and upgrade them yourself. This might not be such a huge
problem from a first glance, but in my opinion many PHP applications and
projects suffer from using either no framework/library or just exactly
one. There is no real cherry-picking going on the PHP world, for example
I would really like to use Zend Framework for the general application
layout, but still use Doctrine for the Modelling and HTML Purifier for
the Output Escaping. Certain tasks might then only be solvable with the
help of eZ Components, all of which are then to some extend dependencies
of my application. With `PEARHUB <http://pearhub.org/>`_ and
`PEARFARM <http://pearfarm.org/>`_ on the horizon (`Read Padraic on this
topic <http://blog.astrumfutura.com/archives/431-The-Democratisation-Of-PEAR-By-Pearfarm-and-Pearhub-or-About-Bloody-Time!.html>`_)
even more PHP code will be distributed using PEAR channels in the near
future. My `immutable
DateTime <http://www.whitewashing.de/blog/articles/124>`_ code for
example makes for a great little open source library that could be
distribued via PEAR, aswell as
`Yadif <http://github.com/beberlei/yadif>`_ - a dependency injection
container I am using extensivly.

Question: Are you really going to manage all these dependencies
correctly manually? Is everything up to date all the time, and
upgradeable with ease?

The PEAR driven solution then begins to look very desirable in this
light, however it has a considerable disadvantage: The PEAR installer
itself works on a system-wide/user-centric basis, making it impossible
to manage dependencies of several applications using only one linux
user. My little `Pearanha <http://github.com/beberlei/pearanha>`_ to the
rescue: I have taken the PEAR installer code (which is distributed with
all PHP installations across all systems) and put a new CLI tool on top
of it. Its a very simple code-generator that allows to generate a
re-configured PEAR installer script which only manages a single
application in a given directory. This approach is also used by the
symfony plugin mechanism, which internally uses the PEAR installer (did
you know?).

Lets revisit my blog application example `from my previous PEAR
post <%3Ca%20href=>`_, first install from
`Github <http://github.com/beberlei/pearanha>`_ and make the "pearanha"
file executable and put it in your PATH (A PEAR Server Channel will
follow any time soon).

Now we need to have an existing application directory somewhere, for
example **/var/www/blog** and then we can put Pearanha on top of it
with:

    ::

        benny@desktop: pearanha generate-project 

You then need to specifiy the project base dir and then the project
style (for example Zend Framework or Manual) which prompts your for the
directory that should be used for as the vendor/library directory that
PEAR will install all the code in. You will also be prompted for a
binary/scripts directory which will then hold a new PHP file for you,
the file **my\_phpiranha**.

**Pro Argument:** Switching to Pearanha can be done at any point in your
application lifecycle. Just define an additional vendor directory for
all the dependencies to go in and generate the applications pear
installer and you are good to go.

The generated script is your new application specific PEAR installer and
you can begin to install all the required dependencies of your
application:

    ::

        benny@desktop:~$ cd /var/www/blog
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha channel-discover pear.zfcampus.org
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha install zfcampus/zf-alpha
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha channel-discover htmlpurifier.org
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha install hp/HTMLPurifier
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha channel-discover pear.phpdoctrine.org
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha install pear.phpdoctrine.org/DoctrineORM-2.0.0
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha channel-discover components.ez.no
        benny@desktop:/var/www/blog$ ./vendor/pear/my_pearanha install ezc/ezcGraph

All this stuff is now located in **/var/www/blog/vendor**. Again you can
use PEARs complete upgrade, remove and install functionality for your
application, now without the hazzle of having to create a linux user for
each project you want to manage this way, which in my opinion is a
considerable simplification. The complete application (including its
dependencies) can then be put under version control and be readily
packaged as a single executable PHAR file by your build process.

As a side node, I did try Pyrus instead of PEAR for the same discussed
purpose, however most of the current PEAR channels don't validate
against Pyrus strict standards for the package.xml file. In the future
this might change and a Pyrus based application installer will then be
integrated into Pearanha.

**UPDATE:** I renamed PHPiranha to Pearanha as its more appropriate.
Also after apinsteins comment on "pear config-create" I rewrote the
generate-project parts to use the config-create functionality
internally, which allowed me to throw away half of the self-written
code. Thanks!
