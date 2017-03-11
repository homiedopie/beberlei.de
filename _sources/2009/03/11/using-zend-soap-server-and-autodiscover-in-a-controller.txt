Using Zend_Soap Server and Autodiscover in a Controller
=======================================================

I am in a dilemma. I have condemned the usage of Zend\_Soap\_Server (or
any other webservice server handler) `inside a Model-View-Controller
application <http://www.whitewashing.de/blog/articles/106>`_ before.
Still I get questions about `my old Zend\_Soap\_Server and
Zend\_Soap\_AutoDiscover
example <http://www.whitewashing.de/blog/articles/65>`_ not working in
the MVC scenario. The following example provides you with a working Soap
server inside a Zend\_Controller\_Action, although I discourage the use
of it and would suggest using a dedicated script outside the dispatching
process to gain multitudes of performance, which webservices often
require.

    ::

        require_once "/path/to/HelloWorldService.php";

        class MyDiscouragedSoapServerController extends Zend_Controller_Action
        {
            public function serverAction()
            {
                $server = new Zend_Soap_Server("http://example.com/pathto/wsdl");
                $server->setClass('HelloWorldService');
                $server->handle();
            }

            public function wsdlAction()
            {
                $wsdl = new Zend_Soap_AutoDiscover();
                $wsdl->setUri('http://example.com/pathto/server');
                $wsdl->setClass('HelloWorldService');
                $wsdl->handle();
            }
        }

Now all you have to do is create two routes, one that makes
**http://example.com/pathto/server** point to
**MyDiscouragedSoapServerController::serverAction** and the other route
that makes **http://example.com/pathto/wsdl** point to
**MyDiscouragedSoapServerController::wsdlAction**. The wrong version
(Version Mismatch) error comes from sending a request for the WSDL file
to the actual Soap Server, which he doesn't like.

.. categories:: none
.. tags:: ZendFramework, SOAP
.. comments::
.. author:: beberlei <kontakt@beberlei.de>
