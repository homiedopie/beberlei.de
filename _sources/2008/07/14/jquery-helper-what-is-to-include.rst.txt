jQuery Helper - What is to include?
===================================

I took some time in the last days to develop the concept for a possible
jQuery View Helper that could pass the integration into the `ZF
Core <http://framework.zend.com>`_. Since
`jQuery <http://www.jquery.com>`_ is organized somewhat different than
Dojo is, its possible implementation for ZF will differ.

The jQuery Helper itself will manage inclusion of jQuery javascript
files and the base library, much like the Dojo component works (Using
the Google CDN). On top of this simple Helpers should mimic $.get,
$.post, $.load and $.getJSON in a simple way, so that with a simple
function call you can generate an XmlHttpRequest that updates a
specified part of the DOM (via injection). (See: `CakePHP
Ajax <http://book.cakephp.org/view/208/ajax>`_)

Problematic are the next ideas: Additional Helpers will allow to
specify the `jQuery UI Library <http://ui.jquery.com>`_ components
(DatePicker, Sortables, Draggable, Dropable..), `jQuery
Autocomplete <http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/>`_
or `jQuery Form <http://malsup.com/jquery/form/>`_ (AjaxForm and
AjaxSubmit). These libraries need additional javascript content to be
downloaded and implemented in the Zend Framework project. There
currently exists no way to implement them using a CDN. Therefore any
documentation must clearly specify which additional content has to be
installed and how. The helpers will have to be general enough to support
this.

My proposal is currently in the workings and will be on the ZF Wiki in
the next couple of hours.

.. categories:: none
.. tags:: ZendFramework, jQuery
.. comments::
