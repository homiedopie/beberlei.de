Doctrine switches from LGPL to MIT
==================================

    tl;dr We moved all the Doctrine PHP projects from LGPL to MIT license
    succesfully in roughly 4 weeks. For that we used a small web-based tool to
    ask the permission of 358 authors that contributed in the last 6 years.

The `Doctrine project <http://www.doctrine-project.org>`_ has been LGPL
licensed since it was started in 2006. When I first started contributing in the
project late in 2009 we were constantly asked about changing the license to a
permissive license such as `MIT <http://en.wikipedia.org/wiki/MIT_License>`_ or
New-BSD.  My subjective feeling is that there are much more libraries with
permissive licenses than 10 years ago. And there are others that `back my
feeling up with facts
<http://news.cnet.com/8301-13556_3-20071811-61/the-open-source-license-landscape-is-changing/>`_.
The fear of getting screwed when using a permissive license has probably
declined in favor of the benefits. `As Lukas puts it
<http://pooteeweet.org/blog/2084>`_:

    Maybe with enough experience you start to realize that it happens close to
    never that a proprietary fork of an open source project ends up outpacing
    the original project.

We wanted all the benefits of permissive licenses as well.  So at the beginning
of this year we as Doctrine project first started to investigate how the task
of switching the license could be done. After a short email with the `FSF
<http://www.fsf.org>`_ it was clear that we had to get the approval of every
single committer or remove their code.

VLC `succesfully attempted a license change
<http://www.videolan.org/press/lgpl.html>`_ last year from GPL to LGPL, so we
we're hopeful to get this done. After discussing with Lukas we came up with the
idea of a tool that helps this process, so `I wrote it
<http://dlm.beberlei.de>`_. It features:

- Import of all commits from one or many Github projects
- Aggregation of commits to authors based on e-mail adress from Git log
- Status approved/not-approved for every author.
- An e-mail engine to send a request for approval to every author using
  `the awesome Mailgun service <http://www.mailgun.net>`_, who has not approved
  yet. We use Mailgun for fun and to have a way to act on bounces easily.
- Admin functionality to mark commits as "trivial or deleted".
- An audit trail to account for all changes and who has done them.
- Symfony2/Doctrine2 application with debian packaging using FPM.

This project is not yet open-sourced but will be when I have some time to clean
up the hardcoded passwords and write a small README on how to adjust the
templates.

After importing the commits of all the LGPL licensed Doctrine projects we
realized that we have 358 unique committers and about 40-50 without an e-mail
address (from the old SVN days). So we started googling for nicknames and
eventually collected all e-mail addresses except maybe 6-8 missing ones.

Now after 4 weeks of bi-weekly e-mail reminders, everyone except 16 committers have
accepted the license change. No single person refused the change. All commits
of the 16 people left we're luckily not part of the code base anymore when we
completly rewrote Doctrine 2 or trivial one-line changes. 

I am very happy to announce that Doctrine is now an MIT licensed project. Have
fun with it.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
