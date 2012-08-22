What will be new in ZF 1.8
==========================

In Februar or March 2009 the 1.8 version of the `Zend
Framework <http://framework.zend.com>`_ is schedulded to be released. I
have contributed some stuff already regarding ZendX\_JQuery and
Zend\_Soap.

Both components have seen numerous bugfixes and I managed to get the
JQuery helper down to zero open issues. I have also taken over the
`Zend\_Json\_Expr
proposal <http://framework.zend.com/wiki/display/ZFPROP/Zend_Json_Expr+to+allow+Javascript+Expressions+(functions)+to+be+encoded+using+Zend_Json>`_,
which will be a huge benefit to everything JSON that can be done with
ZF. Foremost it is an integral part for the jQuery component which
heavily relies on javascript callbacks.

The Soap Autodiscover and WSDL classes compatibility with Java and .NET
has been optimized due to great user feedback, as well as some bugfixes
to the newly added WSDL type detection strategies.

Additionally I went on another bug killing spree and fixed around 20-30
old bugs in a wide range of different components.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>