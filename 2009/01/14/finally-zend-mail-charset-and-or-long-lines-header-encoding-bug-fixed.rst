
Finally: Zend_Mail charset and/or long lines header encoding bug fixed
======================================================================

There was this `lurking bug in
Zend\_Mail <http://framework.zend.com/issues/browse/ZF-1688>`_ which
destroyed every Mail-Header (and corresponding Mail) with non US-ASCII
Chars and more than an encoded length of 74 chars. This is quite a huge
subset of mails, but it seems a nice solution was not so easy, at least
nobody tried to fixed it for quite some time.

Where many hackish solutions we're offered, Ota Mares aka Littlex spent
incredible time to hunt the original problem down and with his help I
tag-teamed the bug to death today. Saturo Yoshida of Zend Fame added
some further spice regarding an alternative solution with Base64
Encoding instead of Quoted Printable Mime Header encoding.

In the end the solution we chose was, not to re-use the Mime encoding
function that is specific to MIME bodies according to
`RFC2045 <http://tools.ietf.org/html/rfc2045>`_, but to write a
completely new algorithm for Mime Headers, whose rules are specified in
`RFC2047 <http://tools.ietf.org/html/rfc2047>`_. This is now done and
unit-tests prove its working according to standard.

What is missing now is people trying that fix on as many Mail platforms
as possible and `giving feedback in the
issue <http://framework.zend.com/issues/browse/ZF-1688>`_ if a lengthy
subject with non-ASCII chars is displayed correctly.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>