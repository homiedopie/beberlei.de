
PHP Conference Recap: NetBeans, ezComponents, MapReduce..
=========================================================

This years october edition of `IPC <http://www.phpconference.de>`_ in
Mainz, Germany was the first php conference I have been to. It ended
some hours ago and i am quite happy to have been there. I had several
great discussions which pointed me to new stuff (to follow) and also met
great people.

First thing that completly fascinated me is `NetBeans 6.5 with PHP
support <http://download.netbeans.org/netbeans/6.5/rc/>`_. It feels much
more easy to use than Eclipse PDT. Its faster (from the little tests i
could make) and does not strike when you add several large libraries
into the include path. It offers much more help on refactoring and
organizing than Eclipse PDT does, for example it offers to generate
getter/setter, constructor, inheritence methods. Much thanks to Petr who
explained to me in detail how NetBeans works.

Ez had lots of people at the conference (to Kore and Tobias i spoke in
more detail) and I had some talks with them about
`ezComponents <http://www.ezcomponents.org>`_. This was especially
interesting after the great session on object persistence in ez, aswell
when I heard that ezcMvc, a model-view-controller component, wil be
included in the next release of ezc in Dezember 2008. ezComponents has a
Database layer, that does not seem to enforce too much overhead on you
but still offers great extensibility through a persistence layer and a
library that offers to build Database Diffs. The latter feature is
really great and I will definatly have a look at this.

Sebastian Bergmann had a great talk on MapReduce which is an old LISP
programming paradigm to work with huge datasets. This style was recently
`revived by Google <http://labs.google.com/papers/mapreduce.html>`_
because tasks can easily be split and distributed for computing on
differend nodes with hundrets of threads. Implementing a working example
in PHP is really easy, just finding a good way to process your large
data seems to be a topic that needs lots of thinking.

Addtional great things:

-  Meet Thomas, the guy that wrote Weaverslave (I use it for years to
   build simple php applications).
-  He is working on a cool open source project `Carica
   Cachegrind <http://sourceforge.net/projects/ccg/>`_ with Bastian
   Feder that will process xdebug cachegrind files via a webinterface
   (They told me webgrind is actually calculating the numbers wrong).
-  Jan Lehnhart and Kore Nordmann had some great things to say about
   `CouchDB <http://incubator.apache.org/couchdb/>`_.
-  Brian Acker talked about `Drizzle <https://launchpad.net/drizzle>`_,
   which is a forked MySQL that throws out lots of legecy stuff from
   MySQL out, to build a micro-kernel database server that suites the
   web.
-  Ulf Wendel talked about Mysqli + Mysqlnd.
   `Mysqlnd <http://dev.mysql.com/downloads/connector/php-mysqlnd/>`_
   will be a new internal driver for PHP to access MySQL through Mysqli
   and optimizes processing and memory consumption. Additionally Mysqli
   will be extended to offer asynchroneous queries that can be fired at
   the database and polled latter. To be included in PHP 5.3

Not so good things: There were absolutly to few power lines. People
using their notebooks were packed on hotspots where power was available.
Please more power plug possibilites next time!

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>