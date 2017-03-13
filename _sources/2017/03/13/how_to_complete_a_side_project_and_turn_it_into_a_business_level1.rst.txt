How to complete a side project and turn it into a business (Level 1)
====================================================================

Almost four years ago I wrote about `Lessons learned: A failed side project
<https://beberlei.de/2013/04/06/a_failed_side_project.html>`_ and when I stumbled
across the post `How to *never* complete anything
<http://ewanvalentine.io/how-to-never-complete-anything/>`_ several days ago I
felt it was time for an update. Ewan's post covers similar lessons learned that I
wrote about in my post and I heard about many side projects since that failed
because of similar mistakes.

There was an argument on HackerNews what a side project is, so I want to
clarify this up front. I am talking about side-projects written with some intend
of turning them into a business, as opposed to side-projects that are started for
learning new technical skills.

Three years ago I have started working on a PHP profiling and monitoring
side-project, which I turned into a business called `Tideways
<https://tideways.io>`_. In this post I wanted to share some of the reasons why
I think this project was successful.

The idea for "XHProf as a Service" was on my "Side Project Ideas" trello board,
where I write everything down that I want to try or experiment with. I have
picked it out for implementation as my new side project, because that month I
would have needed this for a large scale load-testing project at my job with
`Qafoo <https://qafoo.com>`_. It was not the first time I needed this for
myself, I felt a regular pain that a product like this didn't exist.

Not wanting to make the same mistakes, I have applied all the lessons learned from 2013:

- **I picked a small scope**: The first version contained very few features, re-used
  the existing xhprof PHP extension (Tideways now has its own) and instead of a
  daemon collecting data in realtime used a cronjob to collect data from a
  directory every minute. After six months of development I removed half of
  the features I experimented with to reduce the scope again.

- **I did not compete with the established competition on features**, instead I focussed
  on two single features that I thought where the most important: Response time
  monitoring and Callgraph profiling. By focussing on a niche (PHP intead of all
  languages) I was able to provide a better solution than existing generic tools (obviously biased).

- **I did not work all alone on the project**, instead I have immediately enlisted
  alpha-users that gave valuable feedback after 1 month of work and some of
  them are still our most active customers; brought in my employer Qafoo who is
  now a shareholder in the new business; formed business partnerships with
  companies that are now our biggest customers and re-sellers.

- **I did not keep the idea secret**, when I announced our beta program
  publically in June 2015 the launch newsletter list received 250 sign ups and 60
  Twitter followers in a few hours.

- **I choose boring technology**, using a monolithic Symfony, PHP, MySQL
  backend and jQuery frontend stack allowed me to iterate very fast on new
  features with technology that I already mastered. I `spent three innovation
  tokens <http://mcfunley.com/choose-boring-technology>`_ on using Golang for
  the daemon, using Elasticsearch as TimeSeries database and later on learning
  C for the PHP extension.

Making these decisions has not magically turned my side project into a
profit-generating business. However I have avoided all the problems that I have
written about in my failed side project lessons post from four years ago.

The fast iterations on a small scope combined with early user feedback showed
that this idea will work as a business and it was worthwhile to keep pushing
for two years, until the project generated enough revenue after all other costs
to pay my full time salary.

This felt like passing level 1 in getting a bootstrapped side project of the
ground (there are many more levels after that).

.. author:: default
.. categories:: none
.. tags:: SideProjects, Bootstrapping
.. comments::
