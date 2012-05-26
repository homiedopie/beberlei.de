:author: beberlei <kontakt@beberlei.de>
:date: 2010-12-07

Blog Refactorings with Symfony2, Doctrine 2 and Zeta Components
===============================================================

I have been playing around with `Symfony 2 <http://www.symfony-reloaded.org>`_ quite a lot lately and have rewritten this blog using Symfony 2, `Doctrine 2 <http://www.doctrine-project.org>`_ and Zeta Components. You can go over to Github and `find its project page <https://github.com/beberlei/Whitewashing>`_.

Since I have found `Sphinx <http://sphinx.pocoo.org/index.html>`_ I am pretty impressed with Restructured Text and have now integrated that as writing language into my backend. Using `Zeta Components <http://zetacomponents.org/>`_ excellent Document component I transform the written ReST to XHTML. I `hooked into the Document rendering <https://github.com/beberlei/Whitewashing/tree/master/Util/DocumentVisitor>`_ and it now supports using the Sphinx directive ".. code-block:: <language>" and runs the subsequent code through Geshi for highlighting. For example:

.. code-block:: php

    <?php
    echo "hello world with ReST and Zeta Components!";

Using `the jQuery Plugin Tabby <http://teddevito.com/demos/textarea.html>`_ and `MarkitUp with a ReST extension <http://markitup.jaysalvat.com/home/>`_ I can also write more conveniently now. Also to battle spam I have moved the comment system to Disqus.

My next plans for the blog bundle are:

* WebDav support for authoring. All articles will be named "slug.inputformat", for example "blog-refactorings-with-symfony2-doctrine2-zetacomponents.rst". For this I plan to write a custom backend for ezcWebdav.
* Making the Bundle simpler to re-use by others.
* More jQuery love to the backend.
* Trigger some events in the blog post cycle and hook a twitter + facebook notification for new posts in there.

Btw: This blog post is really just a bad excuse for me to test the ReST Editor in the backend. I hope you still enjoyed it ;)
