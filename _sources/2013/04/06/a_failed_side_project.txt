Lessons learned: A failed side project
======================================

Side projects have always been an important part of how I learn new skills and
technologies. This usually ends with me dumping some prototype on `Github
<https://github.com/beberlei?tab=repositories>`_, sometimes even with an open
source project that I commit to maintain over a long time.

Two years ago, for the first time, I pursued a project idea which should
not be open-source but a commercial SAAS product. It grew out of the
`Doctrine <http://www.doctrine-project.org>`_ teams desire to synchronize
Github Pull Requests with our Jira instance: A workflow engine for HTTP
services. `If this, then that (IFTTT) <https://ifttt.com/>`_ already existed at
that point, but was far too limited for my use-case. I wanted something to
allow:

- Accept a Github Pull Request Event
- Open a Jira Ticket
- Comment back on the Pull Request with a link to the Pull Request
- Optionally mention that the Pull Request should be made to master, instead of
  ``$BRANCH``

I started developing this in my free time based on PHP, Symfony2, CouchDB,
PostgreSQL and Backbone.js and got a prototype working early. However
instead of reaching the state where I could release the project to others I
hit some hurdles:

1. The project had a UI where you could add/remove and reconnect tasks through
   a graphical workflow editor. The javascript became very messy fast, because
   I didn't understand Backbone fully and also didn't know patterns for
   decoupling and testing Javascript code.

2. I had to restart with the core domain service side code, because I based it
   on the Zeta Components workflow library and it was too unflexible for my
   special requirements, messing the code up.

3. I wanted to implement way too many features and had a huge backlog of
   issues to implement before "beta".

Last year in July, when I finally had something remotely usable `Zapier
<https://zapier.com/>`_ hit the market with a beautiful product and support
for gazillions of services. At that point my service just had support for
Github, Twitter and Jira and for generic HTTP POST requests and a UI that
could not be operated by anyone else but me. I was quite demotivated
that day I found out about Zapier.

Nevertheless I continued to work on the project and tried to make it even more
powerful than Zapier, by introducing more features that neither IFTTT nor
Zapier had. Adding this complexity ended up being the nail into the coffin of
the project.

Each week I worked less and less on the project, because I couldn't find the
motivation. When Zapier got funded in October I was both sad and happy:
Apparently my idea was a good one, however somebody else executed this idea
much better than myself. I stopped working on the project that week.

Today I took the day to migrate the Doctrine Pull Request workflow to a
`simple hardcoded application <https://github.com/beberlei/githubpr_to_jira>`_
and disabled my projects website entirely.

I want to use this moment to share my personal lessons learnt:

- Choosing a scope that allows you to finish a working prototype within 1-2 months
  is an important key to success.

  The longer it takes to get something working and useable for others, the less
  motiviation you have. I know from my open-source experience that people using your project 
  is a huge motiviation boost.

  The side projects I started since last October are much smaller in scope.

- You can actually get burned out by a side project: by designing its scope
  way too big. 

- You cannot compete feature-wise with startups that put their full attention into
  a project from morning to night. Either make something small working better
  than commercial products or quit your job and put your full time into this.

- Side projects are either about learning new technologies or about trying
  to build something commercially succesful. Don't try to combine this or
  you might get frustrated by choosing the wrong technology for the job.

- Never ever use an existing open-source library as the core of your
  complicated business domain. If your domain is something remotely interesting
  you will fail to achieve your goals with the restrictions of the library.

- Starting a big project alone is not a good idea. I found out that
  discussing ideas with people is very valuable and at the point where I
  started sharing my idea with others I was already too far into the project
  to be able to take most of the advice into account.

- Keeping a project idea secret is completly useless. Others will come up with the
  same idea regardless. People have ideas all the day, however nobody ever has
  time to implement them. When they do, execution is even more important than
  the idea itself.

What are your lessons learnt from failed side projects? I would be happy to
hear other stories.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
