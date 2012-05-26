ezComponents 2008.2 Beta - Mvc separation for win
=================================================

`I have written <http://www.whitewashing.de/blog/articles/88>`_ on the
`new ezComponents MvcTools <http://ezcomponents.org>`_ component before
already. Just yesterday the beta of this component was released with the
`general beta of the 2008.2
version <http://ezcomponents.org/resources/news/news-2008-12-01>`_ of
ezComponents. Several bugfixes and enhancements were included into the
MvcTools which make it a perfect component for any Mvc based
application.

I reviewed lots of the code myself and can only say i love the beauty of
the code. Its very simple but by default the most powerful mvc solution
in the PHP market. People working with unittests will like it very much,
since all the parts are perfectly separated from each other allowing to
test controllers, views, routers and filters in complete separation.

To show one very simple example howto benefit of the seperation of view
and controllers. If we need a view in both html and pdf, this should
generally make no difference for the controller. We add two routes, one
for the pdf one for the html view that execute the same controller and
action:

    ::

        class myRouter extends ezcMvcRouter{ public function createRoutes() {  return array(   new ezcMvcRailsRoute( '/pdf', 'SomeController', 'index'),   new ezcMvcRailsRoute( '/', 'SomeController', index' ),  ); }}class SomeController extends ezcMvcController{ public function doIndex() {  $result = new ezcMvcResult();  $result->variables['items'] = Model::retrieveLotsOfItems();  return $result; }}

Now howto decide between PDF and Html view? We use the createView method
of our dispatcher configuration, but we still only need the http
response writer, nothing more.

    ::

        class myMvcConfiguration implements ezcMvcDispatcherConfiguration { [...] function createView( ezcMvcRoutingInformation $routeInfo, ezcMvcRequest $request, ezcMvcResult $result ) {  if(strstr($routeInfo->matchedRoute, "/pdf")) {   return new myHtmlView( $request, $result );  } else {   return new myPdfView( $request, $result );  } } function createResponseWriter( ezcMvcRoutingInformation $routeInfo, ezcMvcRequest $request, ezcMvcResult $result, ezcMvcResponse $response ) {  return new ezcMvcHttpResponseWriter( $response ); } [...]}

Now both **myHtmlView** and **myPdfView** can create their
ezcMvcResponse objects that fill the response body depending on their
type. Please note that overwritting createResponseBody() in myPdfView is
a shortcut that circumventes me having to write a new PDF View Handler
(which would be the way to go).

    ::

        class myHtmlView extends ezcMvcView { function createZones( $layout ) {  $zones = array();   $zones[] = new ezcMvcPhpViewHandler( 'content', '../templates/index.phtml' );  $zones[] = new ezcMvcPhpViewHandler( 'page_layout', '../templates/layout.phtml' );  return $zones; }}class myPdfView extends ezcMvcView { function createZones() {  // empty, abstract method that has to be defined. } function createResponseBody() {  // Set PDF Content-Type Response Header  $this->result->content->type = "application/pdf";   $pdf = new Zend_Pdf();  // do pdf stuff  return $pdf->render(); }}

Now all the the logic that is potentially in the controller is completly
seperated from the view handling that may depend on the routing
information not on the controller. And views can be tested seperatly
from the controller result. Testability is very high.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>