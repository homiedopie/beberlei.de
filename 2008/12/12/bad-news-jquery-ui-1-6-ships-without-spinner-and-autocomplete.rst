.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Bad news: jQuery UI 1.6 ships without Spinner and AutoComplete
==============================================================

The jQuery UI team `announced yesterday on its
blog <http://blog.jquery.com/2008/12/11/whats-up-with-jquery-ui/>`_ that
`jQuery UI 1.6 <http://ui.jquery.com>`_ will not be shipped with
AutoComplete and Spinner Plugin support. No further delay, for the
orginal august 2008 estimated release, is wanted.

This brings about a problem on
`ZendX\_JQuery <http://framework.zend.com/manual/en/zendx.jquery.html>`_.
All view helpers and decorators that depend on AutoComplete and Spinner
Plugins can only be run with SVN trunk or 1.6 release candidates, which
have known bugs and problems.

I am adding a compability table to the ZendX jQuery manual today that
will make its way to the manual of the 1.7.2 release. This will
hopefully help and guide everyone to the correct dependencies.
