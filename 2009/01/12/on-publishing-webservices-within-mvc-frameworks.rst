
On Publishing Webservices within MVC Frameworks
===============================================

Webservices are a very important part in todays enterprise applications.
They tie applications of different age or programming languages together
or allow applications of different subcontracters to speak to each
other. Because they use HTTP, a stateless network protocol, considerable
overhead floods the pipes when you use them, which should be minimized.

`Martin Fowler <http://martinfowler.com>`_ writes in his `PEAA
book <http://martinfowler.com/eaaCatalog/>`_, that if you have the
option not to use distributed objects (which are implemented via
webservice) you should not distribute them. Considerable effort has to
be brought into keeping complex webservices performant.

Still people make mistakes about webservices all the time (me included
for example proposing a dispatcher for the ZF that could be used for
webservices).

When people report problems with the Zend Soap component they often post
a stripped down example that involes their webservice being instantiated
within a controller. This is a very bad decision based on different
arguments:

-  **Dispatching overhead**: Dispatching, Routing, Pre- and
   Postfiltering is costly in all frameworks. You give up the
   performance of having numerous PHP scripts that act as controller on
   their own. You get centralized filtering, authentication and other
   benefits. But those benefits generally do not aply to XML, JSON or
   SOAP requests, because you cannot parse them or access their
   properties. You give up the performance of a page controller for
   webservices to gain mostly nothing.
-  **HTTP Request uselessness**: Web frameworks work with HTTP request
   objects. The request of webservices facilitates HTTP to act as a far
   more complex request. No framework I know off, allows to work with
   the webservice requests outside the Webservice handler. What a SOAP
   or XML-RPC request does in your MVC is only get passed through
   numerous costly stages that offer no benefit, before it hits the
   target. Only the parsing of HTTP-Headers might offer additional
   benefit, but the gain is low, since they are available to PHP scripts
   at no cost.
-  **Webservices already seperate concerns**: Take the PHP SOAPServer as
   an example. It is an MVC application on its own, the controlling
   aspect of the SOAPServer parses the SOAP Request and sends it to the
   model, a class given by the user, which in turn works and returns the
   result as an SOAP Response View. You have to decouple model and view
   for a webservice handler otherwise it would generate invalid
   responses. Why nest a perfectly separated operation into another one?
   You gain no more of this additional separation, except performance
   decrease.

So what are good practices to implement webservices?

-  Use a page controller that generates no MVC overhead. In context of
   the Zend Framework: Add a new php script to your web root and add a
   new route into your .htaccess file that redirectes the desired
   location of the webservice to the script that overwrites the standard
   catch-all incoming requests to the front controller script.
-  Use the proxy pattern and the invaluable \_\_call() method to
   implement wrapper objects for authentication and session management
   of the webservice. These classes can easily be reused by all
   webservice page controllers of your site. If you do your homework you
   can even share parts of these objects inside your Web-MVC application
   to keep the code DRY. Those proxies keep authentication logic out of
   your service class.
-  Use the remote facade pattern to implement a few, powerful methods
   that delegate the service request to underlying domain objects. Never
   ever publish direct access to domain objects with your webservices.
   As a rule of thumb, talking to a webservice during a logical
   operation should never involve more than one or two calls. The first
   call is for data fetching, the second for data saving. Authentication
   should be handled via HTTP Authentication to save an additional call.

If you follow these simple rules, you should get around the performance
issues that generally come with webservices, without loosing flexibility
at all.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>