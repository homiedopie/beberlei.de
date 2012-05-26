:author: beberlei <kontakt@beberlei.de>
:date: 2009-07-30

PHP CodeSniffer Support for Netbeans
====================================

I dived into the code of my new favorite IDE
`Netbeans <http://www.netbeans.org>`_ these last days and came up with
an `extension
module <http://github.com/beberlei/netbeans-php-enhancements/tree/master>`_,
which adds PHP CodeSniffer Support on a per file basis to make my life
much easier. It shows warnings and errors as annotations to the Editor
and marks the affected lines in yellow and red.

`|image0| <http://cloud.github.com/downloads/beberlei/netbeans-php-enhancements/netbeans_cs_support.png>`_

[STRIKEOUT:My Java skills being very bad, it will only work on Linux
currently, since the PHP Code Sniffer "binary" is hardcoded into the
Java Source code. You have to create a "/usr/bin/phpcs2" executable,
which is a wrapper that looks like:]

With Manuals extensions (see the comments) the module now works without
the wrapper script. It might even work under Windows now. Yet now the
Zend Coding standard is enforced though. I am working on making that one
configurable next.

You can install the `NBM module install
file <http://github.com/beberlei/netbeans-php-enhancements/downloads>`_
from the GitHub repository into Netbeans and it "should" work then.

I hope to get more familiar with Netbeans in the future to add some more
PHP tools and enhance Code Sniffer support.

.. |image0| image:: http://cloud.github.com/downloads/beberlei/netbeans-php-enhancements/netbeans_cs_support.png
