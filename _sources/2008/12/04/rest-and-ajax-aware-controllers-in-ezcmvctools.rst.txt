REST and Ajax Aware controllers in ezcMvcTools
==============================================

There are essentially two major different ways to implement a restful
application using a web framework. You either implement a router that
routes to different controller actions based on the HTTP method used on
a requested resource. This is the fancy way, which sadly is not always
so practical because many browsers do not support sending more than GET
and POST requests. The other way would be to define suburls of a
resource such as **/user/1/delete** for the resource **/user/1** and
take GET a a request for deleting and POST for the confirmation of the
delete.

ezcMvcTools HTTP Request Parser and routing mechanisms currently offer
no real help to decide on this issues, but its easy to extend this
missing functionality. What we first add are simple checks of the
current http request method. We extend **ezcMvcHttpRequestParser** which
will return a derived **ezcMvcRequest** object that implements 7 new
methods: isPost(), isGet(), isDelete(), isPut(), isXmlHttpRequest(),
isMethod() and getMethod(). These methods can now be easily used on the
request object to determine which action will be undertaken:

    ::

        class myMvcRequest extends ezcMvcRequest{  public function isPost()  {    return $this->isMethod("POST");  }  public function isGet()  {    return $this->isMethod("GET");  }  public function isPut()  {    return $this->isMethod("PUT");  }  public function isDelete()  {    return $this->isMethod("DELETE");  }  public function isXmlHttpRequest()  {    if(isset($this->raw['HTTP_X_REQUESTED_WITH'])      && strtolower($this->raw['HTTP_X_REQUESTED_WITH']) == "xmlhttprequest") {      return true;    }    return false;  }    public function getMethod()  {    if(isset($this->raw['REQUEST_METHOD']))      return strtolower($this->raw['REQUEST_METHOD']);    }    return false;  }  public function isMethod($method)  {    if(isset($this->raw['REQUEST_METHOD']) &&       $this->getMethod() == strtolower($method)) {      return true;    }    return false;  }}class myMvcHttpRequestParser extends ezcMvcHttpRequestParser{  /**   * Uses the data from the superglobals.   *   * @return ezcMvcRequest   */  public function createRequest()  {    $this->request = new myMvcRequest;    $this->processStandardHeaders();    $this->processAcceptHeaders();    $this->processUserAgentHeaders();    $this->processFiles();    $this->processAuthVars();    $this->request->raw = &$_SERVER;    return $this->request;  }}

This helps us to implement simple decision mechanisms in a single
controller action that takes both POST and GET requests. From the point
separation of concerns this is not a good design decision. We need
routes that can point to different controller actions based on their
request method, so that two requests **GET /user/1/delete** and **POST
/user/1/delete** lead to different methods, for example
**userController::doDeleteDialog** and **userController::doDelete**. We
will simply extend the **ezcMvcRailsRoute** to support decision based on
http request methods:

    ::

        class myMvcRestRoute extends ezcMvcRailsRoute{  protected $method;  public function __construct( $method, $pattern, $controllerClassName, $action = null, array $defaultValues = array() )  {    $this->method = $method;    parent::__construct($pattern, $controllerClassName, $action, $defaultValues);  }  public function matches( ezcMvcRequest $request )  {    if(strtolower($this->method) == strtolower($request->raw['REQUEST_METHOD'])) {      return parent::matches($request);    }    return null;  }}

This very simple extension is independent of the advanced request parser
given above, so you could use it separately. In the light of our delete
user example, you would use the new router in the following way:

    ::

        class myRouter extends ezcMvcRouter{  public function createRoutes()  {    return array(      new myMvcRestRoute( 'GET', '/users/:id/delete', 'UserController', 'deleteDialog' ),      new myMvcRestRoute( 'POST', '/users/:id/delete', 'UserController', 'delete' ),    );  }}

We have now simple rest route support in our ezcMvcTools application.

.. categories:: none
.. tags:: eZComponents
.. comments::
