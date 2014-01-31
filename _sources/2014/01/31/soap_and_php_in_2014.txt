SOAP and PHP in 2014
====================

    "The SOAP stack is generally regarded as an embarrassing failure these days."
    -- Tim Bray

While the quote by Tim Bray is still true to some degree, the toolstack and
possiblities behind SOAP are still superior to REST in my opinion. REST still
requires alot of manual coding, where RPC with SOAP allows much automation with
tools.

These last years REST has gotten all the buzz, everybody seems to be using it
and there are lots of talks about REST on conferences. SOAP used to be big for
building APIs, but everybody seems to hate it for various reasons. I have used
SOAP in several projects over the last 10 years and this blog post is a random
collection of information about the state of SOAP in PHP 2014, as a reminder
to myself and to others as well.

Why care about SOAP in 2014? For server to server (RPC) communication it still
has massive time to market and stability benefits over REST. The REST toolchain
is just not well developed enough, it lacks:

- a standard to describe the input/output formats of endpoints
- a way to "just do it"
- ways to automatically generate clients in any language

While solutions exist for these problems in the REST space, they are often not
standardized and don't serve the full stack and different languages.

WSDLs for SOAP however allow you to generate servers and clients from
datastructures by the click of a button or execution of a script. I can get two
servers communicating over SOAP, exposing all service methods in literally
minutes.

Basics
------

SOAP is a protocol for Remote-Procedure Calls. HTTP is used as mechanism
to talk between client and servers by sending POST requests with XML request
and response bodies.

The ``SOAPServer`` and ``SOAPClient`` objects ship with PHP core by default.

You can expose functions, classes or objects as server by registering
service callbacks with
``SOAPServer#addFunction``, ``SOAPServer#setClass`` or
``SOAPServer#setObject`` and then calling the ``handle()`` method, which
handles request and response generation and sending in one step. You can
normally exit the request directly after handle.

The client is even simpler, it overwrites the ``__call`` magic method.
Any call to the client therefore looks exactly like the same call
on the server in your code.

PHPs Non-WSDL mode
------------------

One argument against SOAP is the requirement to define WSDL documents for
both server and client to allow communication. This is not true for Clients and
Servers both written in PHP. You can use the non-WSDL mode to expose an object
from the server and use a non-wsdl client to talk to it. The PHP ``SOAPClient``
and ``SOAPServer`` have a common exchange format that is used in this case
and replaces WSDL entirely.

.. code-block:: php

    <?php
    // server.php
    class MyService
    {
        public function add($x, $y)
        {
            return $x + $y;
        }
    }

    $options = array(
        'uri' => 'http://server/namespace',
        'location' => 'http://server/location',
    );

    $server = new SOAPServer(null, $options);
    $server->setObject(new MyService());
    $server->handle();

The client is as simple as the following lines of code:

.. code-block:: php

    <?php
    // client.php
    $options = array(
        'uri' => 'http://server/namespace',
        'location' => 'http://server/location',
    );
    $client = new SOAPClient(null, $options);
    echo $client->add(10, 10);

This kind of services work with flawlessly all datatypes except with objects,
which get converted to ``stdClass`` with public properties on the Client.

If you are developing internal APIs between components in your own system,
then using SOAP in non-WSDL mode is a massive time saver. You can expose
remote services for Remote procedure calls this way very easily.

The only downside is that you have no documentation what methods exist on the
client and **ALL** public methods of the server object can be called, so make sure
they only have those methods you want to be called remotely.

Debugging SOAP
--------------

When something goes wrong in either the client or server, it sucks to debug
these problems. In general there are several mechanisms to debug SOAP in PHP:

1. Enable ``'trace' => true`` option on the SOAPClient. This allows you
   to call the methods ``$client->__getLastResponse()`` and
   ``$client->__getLastRequest()`` to take a look at the interaction between
   server and client.

2. When failures happen, ``SOAPClient`` throws a ``SOAPFault`` exception.
   You can even throw this exception yourself from the SOAPServer code,
   and the client can then read this failure. However you must know
   that the ``$faultcode`` variable in the constructor of ``new
   SOAPFault($faultcode, $faultmsg)`` is **NOT** an integer error code
   like in normal Exceptions. Instead its either a value ``SERVER`` or ``CLIENT``,
   with the component of the interaction that failed.

3. If you throw non ``SOAPFault`` exceptions from the server, then you
   need to catch them and recast them to ``SOAPFault``, otherwise
   the client only sees "Internal Server Error" messages.

You can easily solve the ``SOAPFault`` problem by decorating your service with an exception handler,
and also logging the errors yourself.

.. code-block:: php

    <?php

    class SoapExceptionHandler
    {
        private $exposeExceptionMessages = array(
            'MyProject\DomainException',
        );

        private $service;

        public function __construct($service)
        {
            $this->service = $service;
        }

        public function __call($method, $args)
        {
            try {
                return call_user_func_array(
                    array($this->service, $method),
                    $args
                );
            } catch (\Exception $e) {
                // log errors here as well!
                if (in_array(get_class($e), $this->exposeExceptionMessages)) {
                    throw new SOAPFAult('SERVER', $e->getMessage());
                }

                throw new SOAPFault('SERVER', 'Application Error');
            }
        }
    }

    $server = new SOAPServer(null, $options);
    $server->setObject(new SoapExceptionHandler(new MyService()));
    $server->handle();

Generating WSDLs
----------------

SOAP uses a service description format called WSDL to describe the input and
output of the server and what methods exist. WSDL are formatted with XML
and use XMLSchema to describe the input/output messages. The format is very
complex, however tools for any languages allow you to autogenerate WSDLs
from code.

There are several reasons to introduce WSDLs for your SOAP service:

- Your SOAP clients will not be written in PHP, which prevents use of the non-WSDL mode.
- Clients of the service are used and  written by other teams or companies.
- You want to use the WSDL as a validation mechanism for input from clients.

While you should have some understanding of how a WSDL looks like,
you should never write it manually. I use `Zend Frameworks SOAP Autodiscovery
<http://framework.zend.com/manual/2.0/en/modules/zend.soap.auto-discovery.html>`_ for this.
By default it uses the docblocks ``@param`` and ``@return`` to generate
the correct WSDL for a service:

.. code-block:: php

    <?php
    $autodiscover = new Zend\Soap\AutoDiscover();
    $autodiscover->setClass('MyService')
                 ->setUri('http://server/namespace') // same as server 'uri'
                 ->setLocation('http://server/soap.php') // same as server 'location'
                 ->setServiceName('MyService');
    $wsdl = $autodiscover->generate();
    $wsdl->dump("/path/to/file.wsdl");

You can now place that WSDL file in any public location and then point both
``SOAPServer`` and ``SOAPClient`` at the file using the first constructor
argument:

.. code-block:: php

    <?php
    $server = new SOAPServer('http://server/path/wsdl', $options);
    $client = new SOAPClient('http://server/path/wsdl', $options);

To make the WSDL generation work with objects and object graphs, you have
to use objects in your service API that have only public properties. If
you dont do it this way, you will need to convert the objects in a seperate
step, something to avoid.

Sometimes you want to use other metadata than docblocks. When using
tools like Doctrine you already now much better what datatypes an object has.
You can write your own `ComplexTypeStrategy` to generate the metadata
for your WSDL files. This is more advanced topic, but can be understood and
automated in a reasonable amount of time.

Generating Objects from WSDL
----------------------------

If you implement a client, you want to generate objects for the datastructures
of a WSDL file. You can use those objects instead of the ``stdClass`` objects
which are used by default.

For this task I use the `XSD-TO-PHP library
<https://github.com/moyarada/XSD-to-PHP>`_.  I normally hack around in the code
a little to adjust for correct namespace generation and code-style adjustments,
but it works quite well by default. Here is an example of a generated class
for the DHL Intraship SOAP API:

.. code-block:: php

    <?php
    namespace DHL\Intraship;

    class Person extends ComplexType
    {
      /**
       * 
       * @var salutation $salutation
       * @access public
       */
      public $salutation;

      /**
       * 
       * @var title $title
       * @access public
       */
      public $title;

      /**
       * 
       * @var firstname $firstname
       * @access public
       */
      public $firstname;

      /**
       * 
       * @var middlename $middlename
       * @access public
       */
      public $middlename;

      /**
       * 
       * @var lastname $lastname
       * @access public
       */
      public $lastname;
    }

The next thing you can generate is a classmap, that maps every WSDL Type to
your newly generated code, in the above example:

.. code-block:: php

    <?php

    $client = new SOAPClient($wsdl, array(
        'classmap' => array(
            'Person' => 'DHL\Intraship\Person',
            // all the other types
        )
    ));

SOAP with different Languages
-----------------------------

As long as you stay within the PHP world, SOAP is rather easy with both WSDL
and non-WSDL modes. Once you want to talk to Java or C# you need solve some
more problems.

The first thing to understand is that SOAP can actually talk in 4 different
modes. You can use 'document' or 'rpc' style, 'literal' or 'encoded'  use.
This post on the `IBM website
<http://www.ibm.com/developerworks/library/ws-whichwsdl/>`_ describes all the
different modes in much detail and I recommend everybody having to work with
SOAP to read it.

The essence from that article is, that you will always want to use
`document/literal` for your SOAP services, to be compliant with all languages,
wrapping each method call and response in its own Message Document.

However using this style is rather complicated in PHP itself, because
for every input and output message you need to create a wrapper object (or
array) with a specific structure.

You can fix this problem on the Server by using this `DocumentLiteralWrapper
<https://github.com/zendframework/zf2/blob/master/library/Zend/Soap/Server/DocumentLiteralWrapper.php>`_
class in Zend Framework 2. It has no external dependencies, so you can just
copy it into your project if you want.

To generate a WSDL for document/literal mode, use the following methods
on Zend Autodiscovery:

.. code-block:: php

    <?php
    $autodiscover = new Zend\Soap\AutoDiscover();
    $autodiscover->setBindingStyle(array('style' => 'document'))
                 ->setOperationStyle(array('use' => 'literal'));

Then use the wrapper like such:

.. code-block:: php

    <?php

    $server = new SOAPServer($wsdl, $options);
    $server->setObject(
        new \Zend\Soap\Server\DocumentLiteralWrapper(
            new SoapExceptionHandler(
                new MyService()
            )
        )
    );
    $server->handle();

SOAP Servers generated this way can be converted into a C# SOAP Client with a
bunch of button clicks from Visual Studio. It will generate both the Client
object and all the data transfer objects for you. Truely amazing.

Testing SOAP Interaction
------------------------

Because SOAP is very painful about the exact format of messages and rejects
invalid messages in the client already when they do not match the WSDL you
certainly want to Integration test your clients and servers.

You can do that in PHPUnit by using a client, that wraps a Server directly
and doesn't require a Webserver. Zend Framework 2 already has such an object,
named `Zend\Soap\Client\Local`. Its usage is simple:

.. code-block:: php

    <?php

    $server = new SOAPServer($wsdl, $options);
    $server->setObject(
        new \Zend\Soap\Server\DocumentLiteralWrapper(
            new SoapExceptionHandler(
                new MyService()
            )
        )
    );
    $client = new \Zend\Soap\Client\Local($server, $wsdl);
    $client->add(10, 10);

This will pass through the complete SOAP marshalling and unmarshalling
process and allow you test SOAP interaction.

If you want to take a look at the code of the Local client, `its very easy to
achieve this
<https://github.com/zendframework/zf2/blob/master/library/Zend/Soap/Client/Local.php>`_.

Versioning with SOAP/WSDL
-------------------------

If you want to version your SOAP Service, you will need to provide versioned
WSDL files on different URLs. You should never change the WSDL at a location,
because languages like C# statically create clients from the WSDL, never
talking to the WSDL again.

If you take care of your Service objects, then you can design them in a way
that you can use the same PHP service object for many different versions of the
WSDL file in a backwards compatible way. If your API changes alot, you might
need to implement different PHP service classes to allow for versioned APIs.

Conclusion
----------

While the full extent of SOAP and WSDL can be scary, they allow you to write
servers and clients for RPC communication between servers and languages very
easily. If you don't need to expose your API to the webbrowser via REST/JSON,
then using SOAP is a very good alternative to most of the handcrafting that is
necessary for REST APIs.

.. author:: default
.. categories:: PHP
.. tags:: PHP
.. comments::
