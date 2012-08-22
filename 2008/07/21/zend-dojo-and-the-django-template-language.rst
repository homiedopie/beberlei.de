Zend, Dojo and the Django Template Language
===========================================

With the Zend Framework `nearing its 1.6
release <http://www.nabble.com/1.6-RC1-Schedule-tp18538148p18538148.html>`_
and full `Dojo Toolkit <http://www.dojotoolkit.org>`_ support I took
some time to look up what Dojo is actually capable of. I found the
`DojoX Django Template
Language <http://dojotoolkit.org/book/dojo-book-0-9/part-5-dojox/dojox-dtl>`_
extension and remembered my neighbor talking about why Python + Django
is so much better than PHP with any other framework. So I digged into
the `Django template
language <http://www.djangoproject.com/documentation/templates_python/>`_
and found that it is quite awesome.

Variable filtering and evaluation looks almost like Smarty the syntax
being {{var.key\|filter1\|filter2:"arg1":"arg2"}}. The logical syntax is
quite different though, taking an somehow object oriented view on
templates you can extend an existing template and override specific
parts with your more special implementation. Have a look at the
following two snippets:

    ::

        This is an example of Django template inheritance:

        {% block helloworld %}Hello World!{% endblock %}

    ::

        {% extends "base.html" %}

        {%block helloworld %}Hello World for Object Oriented Views!{% endblock %}

What does Django do with this second template when rendering? It
realizes it inherits logic from a parent template and substitutes all
special blocks for the parent ones. With a little object oriented
background you can guess the result looks like this:

    ::

        This is an example of Django template inheritance:

        Hello World for Object Oriented Views!

So what was all the talking about Dojo being able to parse this kind of
templates? If you envision a helper component that would function like
this: 1.) make an ajax request to $url 2.) retrieve json object from the
controller 3.) render json object with $template into container
$container. The helper would know that the template is needed in this
HTML response and appends it to the Dojo Helper output. A link would be
generated performing steps 1 and 2, handing over the json data to the
template and render the output. What do you get? Templates that can be
used Client and Server side.

For example on rendering the view of your blog you can send all the
comments using a specific comment building Django template script.
Additionally you can also use the same template to render any new
comment to the comment list using via an ajax form submit, returning the
(model or form) filtered data via JSON and appending it to the comment
list using the DojoX DTL parser. For non-JS browsers you can always use
a <noscript> variant to render the templates completely server-side.

This generally being a cool idea since it makes developing applications
with AJAX technology very easy I began to port the DTL to the Zend
Framework and the whole weekend later I got a working implementation
that supports at least the "extends", "for", "include", and "comment"
tags. As a next task I will implement the helper for DojoX DTL and will
report back on my efforts.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>