.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

On Frameworks and Javascript Coupling
=====================================

`Zend <http://www.zend.com>`_ announced they work together with the
`Dojo Team <http://www.dojotoolkit.org>`_ to integrate Javascript
support into the Zend Framework. What this actually means is that you
can write your Javascript Code in PHP if you're javascript library of
choice is Dojo.

Since Dojo is not my library of choice I would have to write a JQuery
View Helper on my own or wait until somebody else releases one.

But why not write javascript? Its very easy with all those libraries and
addresses most cross browser incompabilities: `One
Django <http://www.b-list.org/weblog/2006/jul/02/django-and-ajax/>`_,
`one Zend Framework
developer <http://www.builtfromsource.com/2006/12/20/does-ajax-have-a-place-in-the-application-framework/>`_
argue framework and javascript coupling is not the way to go based on
the arguments that its breaks the MVC pattern, leads to function calls
equal to those in javascript in its framework respective language, and
that javascript is actually something any good webdeveloper should be
able to programm, even when its just using library components.

Using `JQuery <http://jquery.com>`_ without any help from tools for
about a year now I can say there are still those days where javascript
drives me mad, but most of the time I its working perfect. Since Ajax
related calls like GET, POST, and FORM stuff are oneliners I don't see
why one would need tighter integration of JS and frameworks.

Larger Javascript components like Popup Calendars, Autocomplete and the
like are harder to integrate than in Rails or cakePHP, but thinking
about the problem a little longer leads to powerful reusable solutions,
that save time on integration after the first initial setup.
