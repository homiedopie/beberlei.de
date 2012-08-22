Zend_Form - Rapid Development Plugin for Eclipse?
=================================================

I found some time in the last weeks to reconsider `Zend
Framework <http://framework.zend.com>`_, this time in the 1.5 version,
for this blog software and rewrote all Forms using the new Zend\_Form
component. I have to say, i love it. Its very easy using the already
existing Zend\_Validate and Zend\_Filter components as input for the
generated form fields. Another plus is the handling of errors in input
and re-entering/displaying text.

There is also a neat feature of the Zend\_Form component, which allows
to `generate complete forms by passing an appropriately formatted
Zend\_Config\_Ini object to the Zend\_Form
Constructor <http://framework.zend.com/manual/en/zend.form.quickstart.html#zend.form.quickstart.config>`_.
So my idea was, why not program an Eclipse Plugin allowing to rapidly
generate and edit forms using a point-and-click plugin window approach,
which would ultimately generate your Form INI code.

This might have been a great `Google Summer of Code
idea <http://code.google.com/soc/>`_ for the Eclipse Foundation (since
Zend is not taking part).

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>