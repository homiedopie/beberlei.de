.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Complete Django Template Engine Implementation for PHP5 - Downloadable Now
==========================================================================

I prepared a downloadable version of my `Django Template
Language <http://www.djangoproject.com>`_ Engine Clone for PHP5 and the
Zend Framework (although it can easily be used Standalone). It also
implements two helpers that aid in rapid ajax/Dojox deployment. You can
easily specify template blocks that should be rendered by Javascript via
DojoX DTL, which are then marked, compiled and shown by the client using
JSON data from the server. I included a demo to show this feature.

You can grab the
`Tarball <http://www.beberlei.de/sources/calypso-dtl-0.1.tar.gz>`_ and
there is also a
`README <http://www.beberlei.de/sources/README_Dtl.txt>`_ with some
information. I would appreciate if anbody would test the lib and gave
some feedback.

I will soon start to push this component in the ZF proposal process. I
still have to finish the class structure before I can move to the Ready
for Review stage. The library will max end up in Zend Extras. Therefore
I will have to say again: This View Renderer shall be no replacement for
the current Zend View. It is only an alternative which allows for some
neat functionality and stricter View / Controller logic seperation.

**UPDATE:** I finished a little page for what I call the Calypso DTL.
See it here: `Calypso Site <http://www.beberlei.de/calypso/>`_. I have
put up a little tutorial how to get the Template Engine running with
Zend Framework and as a standalone component.
