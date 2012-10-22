A tent.io app: Zelten Bookmarks
===============================

Over the weekend I built a `very simple bookmarking application
<http://zelten.eu1.frbit.net>`_ for `tent.io
<http://tent.io>`_. I wanted to try the tent functionality to create
arbitrary entities of data using something as simple as a "Bookmark".

The application retrieves and stores bookmarks on your own tent-server, nothing
is kept on the applications server and as a user you keep full control over
your content (bookmarks). 

The `code for the application <https://github.com/beberlei/zelten-bookmarks>`_
is on Github, as well as the `TentPHP library
<https://github.com/beberlei/TentPHP>`_ I have written to support the protocol.
The application is using PHP, the Silex microframework and MySQL.

So what is Tent and why bother?
-------------------------------

About two month ago a new distributed social networking protocol was launched called
`Tent.io <http://tent.io>`_. It works over HTTP using JSON and distributes data
using webhooks. This happened in the shadow of `app.net <http://www.app.net>`_
funding, just two weeks after they collected over 500k USD. Tent.io got lots of
attention but not as much as app.net sadly. Its distributed nature however is
much more suited to achieving true independence of large companies and true privacy
for the users though. Compared to Diaspora it has the benefit of being a protocol, not
an application first.

Now two month later, there are `reference implementations <https://github.com/tent>`_
for Server, Client and a Twitter like Status application. You can use `Tent.is
<http://tent.is>`_ to create a free or payed tent account including access to
the status application or setup your own tentd server on Heroku.

As a user I can connect any application to the tent server I have registered
with and control the visibility and sharing policies. Content can be private,
public or visible to certain groups only. A Tent server then makes sure to
distribute content to the appropriate subscribers.

In this early state of the protocol it makes sense to register on the central
tent.is service, however when the server gets more stable or alternative
server implementations popup its easy to move all your data off tent.is to your
own server. One feature that will hit tent.is soonish is registration of domain
records. That will be the first step to your own tent server, I am eagerly
waiting to host all my content at https://tent.beberlei.de at some day.

Tent.io sounds awesome, how can I help?
---------------------------------------

Right at the moment the tent software stack is developed by the team that also
hosts `Tent.is <https://tent.is>`_. If all you can provide is money, then
signing up for the 12 USD per month is the way to go.

If you are a developer, then take a look at the `Wiki
<https://github.com/tent/tent.io/wiki/Related-projects>`_ where related
projects are listed. You will find a bunch of client libraries for major
languages already, helping you to get started.

I suppose the major work lies in implementing Status-Post clients for all
major smartphone platforms and desktops. As well as the host of applications
that Facebook and other social networks provides:

- Manage and share Photo albums
- Plan and share events
- Managing contact data/address book
- Resume details (Linkedin/Xing)
- Track User Events (Timeline)
- Sharing Music and Videos (Myspace)
- Importing all sorts of existing content (RSS,..)

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
