
Performance in Calypso (and Bugs)
=================================

I have tested Calypso performance some weeks ago and have not been able
to write on it before. Don't use it please its fucking slow and cannot
be optimized in the current architecture, because the template will NOT
be parsed into intermediate PHP code.

Additionally there are some bugs:

#. You cannot currently use UTF8 encoding since htmlentities deep in the
   escape mechanism cannot be given the utf-8 specification.
#. Triple or higher inheritence may not work under some circumstances.
   Which sucks.

I sadly have no time currently to fix any of the issues poping up with
Calypso, so please don't use it for anything production.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>