Discussing a jQuery Helper for Zend Framework
=============================================

Yesterday I had some time to test Matthews `Dojo View
Helper <http://framework.zend.com/wiki/display/ZFPROP/Zend_View_Helper_Dojo>`_
and the Zend\_Dojo\_Form component. At a first glance the implementation
looks great and can almost instantly generate you a very nice form with
all the possible Dijit form extensions that
`Dojo <http://dojotoolkit.org/>`_ has to offer.

If one were to refactor the Dojo Component to allow for
`jQuery <http://www.jquery.com>`_ elements one bigger problem appears.
Dojo has a CDN (Content Distribution Network) for all its components,
that is, the Zend Dojo components can load all javascript and css files
from a distant server. JQuery can only offer its main library to be
loaded from a CDN. All additional components, for example the jQuery
DatePicker, have to be installed locally. This significantly reduces the
possibility for rapid development of Javascript/Ajax/Form components
with jQuery and Zend Framework.

One could offer a complete dependency downloadable archive with all the
CSS, Javascript and Images inside, but this would be very complex to
maintain. Looking at the future Zend Tool capabilites one possibilty
would be to offer a download client for all the relevant jQuery plugins,
but there would have to be a man-middle-server that maintaines the most
up to date locations of all the plugins, which also has to be
maintained. Does anybody have a better solution to solve this problem?
Perhaps the jQuery Team needs to be made aware that they need a CDN for
their most stable plugins.

Abstracting from the CDN problem, I implemented a simple jQuery View
Helper (mostly copy paste and simple rewrites from Matthews Dojo
component) and a HtmlElement Form Helper which constructs a Date-Picker
from within the template. This is very easy to use and looks great. In
the next days I will add further helpers for the jQuery plugins I use in
my day to day work live and hope to present a demo. I might even optin
for a jQuery proposal aiming at inclusion in the Zend Extras Library.

**Update:** I got a `reply on the jQuery mailing
list <http://groups.google.com/group/jquery-dev/browse_thread/thread/aec0d89b97a95880>`_
stating that a CDN is planned for the jQuery UI library. Sadly this does
not include plugins for which one might desperatly need a View Helper
except for maybe the Date Picker. I will post further comments on this
issue in the near future.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>