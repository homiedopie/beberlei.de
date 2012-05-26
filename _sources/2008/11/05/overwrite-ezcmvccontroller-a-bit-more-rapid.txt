Overwrite ezcMvcController - A bit more rapid
=============================================

ezComponents gets Mvc in its 2008.2 version. I have played around a bit
with the alpha version, since I am currently searching for a good
framework for a high performance application. My first benchmarks on
ezcMvc just say: wh000pie! Alot faster as compared to the Zend
Framework.
Still ezcMvc is VERY loosly coupled and you have to write lots of lines
to get where ZF gets you with less (more magic involved). As you can see
from the `tutorial on the ezcMvcTools
component <http://ezcomponents.org/docs/tutorials/MvcTools#creating-the-controller>`_
it is currently a bit unwieldily to work with ezcMvcController since you
have to create and return result objects everywhere. This is very nice
since it abstracts from the actual response type (could be www, mail,
cli, anything).
I have created a very little extension of the ezcMvcController class
that hopefully serves you quite some time. You can append variables to
the ezcMvcResult object by calling the magic \_\_get and \_\_set on the
controller. Plus it offers a method to use the ezcMvcInternalRedirect
instead of the result. See for yourself:
    ::

        class myController extends ezcMvcController
        {
            protected $result;

            public function createResult()
            {
                $actionMethod = $this->createActionMethodName();

                if ( method_exists( $this, $actionMethod ) ) {
                    $status = $this->$actionMethod();
                    if($status != 0) {
                        $this->getResult()->status = $status;
                    }
                    return $this->getResult();
                } else {
                    throw new ezcMvcActionNotFoundException( $this->action );
                }
            }

            protected function _redirect($uri)
            {
                $request = clone $this->request;
                $request->uri = $uri;
                $this->result = new ezcMvcInternalRedirect($request);
            }

            public function __get($name)
            {
                if(isset($this->getResult()->variables[$name])) {
                    return $this->getResult()->variables[$name];
                }
                return null;
            }

            public function __set($name, $value)
            {
                $this->getResult()->variables[$name] = $value;
            }

            public function __isset($name)
            {
                return isset($this->getResult()->variables[$name]);
            }

            protected function getResult()
            {
                if($this->result === null) {
                    $this->result = new ezcMvcResult();
                }
                return $this->result;
            }
        }

You can now use a controller in the following way:

    ::

        class dashboardController extends myController
        {
            public function doIndex()
            {
                $this->cookie = "Cookie!"; // Proxy to $ezcMvcResult->variables['cookie']
            }

            public function doRedirect()
            {
                $this->_redirect("/");
            }
        }

Very nice! The next thing I have to extend in ezcMvc is automagical
matching of controller and action names to view output names with a
special View Handler that takes care of this. This saves another bunch
of work you have to cope with in the current standard setup.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>