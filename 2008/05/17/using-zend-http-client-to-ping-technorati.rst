Using Zend_Http_Client to Ping Technorati
=========================================

Send a ping to Technorati manually is a pain in the ass. Writing a
little Method that handles this functionality for your own blog software
is quite easy. Call the following method after you created or updated a
post of yours:

    ::

        private function _pingTechnorati()
        {
            $xml = $this->view->render('ping_technorati.phtml');
                    
            $httpclient = new Zend_Http_Client('http://rpc.technorati.com/rpc/ping');
                    $httpclient->setHeaders('User-Agent', 'PHP/Zend Framework/Zend_Http');
                    
            $httpclient->setRawData($xml, 'text/xml')->request('POST');
                    
            $response = $httpclient->request();
                    
            if($response->isSuccessful() === true) {
                return true;   
            } else {
                return false;   
            }
        }

You also need a little view in XML format like it is described in the
`Technorati Ping Configuration
Guide <http://technorati.com/developers/ping/>`_ and ready to go you
are!

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>