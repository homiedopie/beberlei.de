ZF 1.7: jQuery is in! Zend_Soap with lots of Bugfixes.
======================================================

The next version of `Zend Framework <http://framework.zend.com>`_ will
appear quite soon (16th November) and there will be lots of buzz about
Zend Amf, the new component sponsored by Adobe to support Adobe Flash
(or other tools) to PHP communications.

Besides the buzz there is some stuff from me getting into the Zend
Framework. jQuery View and Form Helpers will allow you to throw the Dojo
stuff away and use the great jQuery. This is of course inherently
subjective, but still different opportunities are always great.

Additionally I have been fixing quite some bugs on the Zend Soap
component and will manage to fix further stuff until the 1.7 release I
hope. This will make especially Wsdl and AutoDiscover produce valid WSDL
XML plus adds setObject() support to ``Zend_Soap_Server``.

You can now choose between several strategies to evaluate complex types
in WSDL Autodiscovering. Array of Datatypes (simple or complex) via
type[] syntax and complex objects can be parsed differently now based on
settings.

.. categories:: none
.. tags:: ZendFramework, SOAP
.. comments::
