First impressions on Zend_Soap and a basic implementation
=========================================================

The `Zend Framework <http://framework.zend.com>`_ release candidate for
version 1.6 includes a new component for SOAP operations.
`Zend\_Soap\_Server/Client <http://framework.zend.com/manual/en/zend.soap.html>`_
extend the PHP functionality of the SOAPClient and SOAPServer objects,
which by itself is trivial. The more important functionality it ads to
the package is the `AutoDiscovery
Component <http://framework.zend.com/manual/en/zend.soap.autodiscovery.introduction.html>`_.

Generally you can use `SOAP <http://en.wikipedia.org/wiki/SOAP>`_ in the
so called "non-wsdl" mode, that is if you specify the correct options
like the soap service location and uri, you don't need any description
of the service for the clients. This is only useful if you're using the
SOAP Service internally since you then know about all the available
functions and methods. If you want to offer the Service for external
users you want to use the WSDL-mode: Generate a
`WSDL <http://en.wikipedia.org/wiki/Web_Services_Description_Language>`_
that describes the services available methods, their parameters and
return types is an important task.

Using Zend\_Soap\_AutoDiscover you can generate your WSDL file
automatically by reflecting on the given Service Class methods. This
works as follows. We setup a simple service:

    ::

        class HelloWorldService
        {
            /**
             * @return string
             */
            public function helloWorld()
            {
                return "Hello World!";
            }

            /**
             * @return array
             */
            public function getFruits()
            {
                return array('apple', 'orange', 'banana');
            }
        }

It is important that you specify the Doc Comments @param and @return
otherwise the AutoDiscovery of the correct parameter and return types
cannot be resolved. We will now setup a simple SOAP Server access point,
that will also generate our WSDL file for description of this HelloWorld
service:

    ::

        require_once "HelloWorldService.php";
        require_once "Zend/Soap/Server.php";
        require_once "Zend/Soap/AutoDiscover.php";

        if(isset($_GET['wsdl'])) {
            $autodiscover = new Zend_Soap_AutoDiscover();
            $autodiscover->setClass('HelloWorldService');
            $autodiscover->handle();
        } else {

            $soap = new Zend_Soap_Server("http://localhost/soapserver.php?wsdl"); // this current file here
            $soap->setClass('HelloWorldService');
            $soap->handle();
        }

Now we have our SOAP Service up and running and any client can access
the HelloWorldService class from a remote or local location with just
this simple lines:

    ::

        require_once "Zend/Exception.php";
        require_once "Zend/Soap/Client.php";

        try {
            $client = new Zend_Soap_Client("http://localhost/soapserver.php?wsdl"); // Servers WSDL Location
            $string =  $client->helloWorld();
            $fruits = $client->getFruits();

            var_dump($string);
            var_dump($fruits);
        } catch(Zend_Exception $e) {
            echo $e->getMessage();
        }

    This is easy. Additionally Zend\_Soap offers a WSDL class to
    generate your own WSDL file based on your special preferences, which
    is a nice feature. I guess only some people can write a correct WSDL
    XML specification file on their own from scratch, so using a
    powerful helper is reasonable.

    The usage of Zend\_Soap is quite simple and straightforward as is
    PHP5's internal SOAP Service and might therefore gain widespread
    use. I have never tested PEAR's WSDL Autodiscovery, so i cannot draw
    comparisons.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>