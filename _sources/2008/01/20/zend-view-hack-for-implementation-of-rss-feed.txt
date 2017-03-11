Zend_View Hack for implementation of RSS Feed
=============================================

Using Zend\_View for your site and want to implement an RSS Feed? You
might run into the problem that the XML header definition is interpreted
as PHP code:

.. code-block:: php

    <?xml version="1.0" encoding="ISO-8859-1"?>

Before you start cursing the world try this (rather obvious) workaround:

.. code-block:: php

    <?php echo '<?xml version="1.0" encoding="ISO-8859-1"?>'; ?>


.. categories:: none
.. tags:: ZendFramework
.. comments::
