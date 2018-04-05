PHP CodeSniffer for Netbeans v0.2
=================================

I finally found some time to spend some time on the `PHP CodeSniffer for
Netbeans
plugin <http://github.com/beberlei/netbeans-php-enhancements/>`_.
Previously the plugin used an unnecessary API which restricted the use
to Netbeans 6.7.0 only. This API was removed so that the plugin should
now work with all Netbeans Versions >= 6.7.0.

Additionally when working the previous version would scan every PHP
script on a file per file basis when the all projects or main projects
filters were activated. This rendered made the plugin almost useless. In
the current version scans of filters that contain more than one file are
blocked. That means you will only see Coding Violations when you enable
the "Current File" filter. Using any other filter will just do nothing
and won't put your Netbeans in permanent hibernation mode (aka useless
mode).

There is also some preference **"phpcs.codingStandard"** using the
**`NbPreferences
API <http://bits.netbeans.org/dev/javadoc/org-openide-util/org/openide/util/NbPreferences.html>`_**
which allows to configure the coding standard. [STRIKEOUT:However this
feature was contributed by Manuel Pichler and I don't yet understand how I can
manipulate it. Maybe someone knows how (\*Looking in Mapis general
direction\*)?] By default the Zend Coding Standard is used.

**Update:** Coding Standard can be changed by hacking into the config
file .netbeans/6.7/config/Preferences.properties setting
"phpcs.CodingStandard=". Additionally I fixed several bugs with the
inline highlighting that did not refresh when lines in the file changed.

.. categories:: none
.. tags:: Netbeans
.. comments::
.. author:: beberlei <kontakt@beberlei.de>
