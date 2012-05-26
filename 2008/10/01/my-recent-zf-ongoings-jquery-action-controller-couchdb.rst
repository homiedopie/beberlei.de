My recent ZF ongoings: JQuery, Action Controller, CouchDb
=========================================================

In the last weeks lots of stuff came up for me regarding the Zend
Framework. My `jQuery <http://jquery.com>`_ component is finished, i
have even commited the documentation into the SVN already. Do read it
you have to be either an XML fetishist or compile it using a docbook
compiler. Lots of questions about ZF and jQuery come up regularly on the
mailing lists so I really look forward for the first ZF 1.7 release
candidate which will include the helpers for a broader audience. This
component comes at a good point, since `a few days ago the jQuery team
announced a deal with Microsoft and
Nokia <http://jquery.com/blog/2008/09/28/jquery-microsoft-nokia/>`_.
Microsoft will include jQuery as the framework to go into its Webbased
ASP.Net applications and Nokia will include the library in their mobile
phones.

Additionaly i reported an `important issue
(ZF-4385) <http://framework.zend.com/issues/browse/ZF-4385>`_ that
offers a patch to create an interface of the Action Controller and
therefore allows everyone to implement their own action controller
classes. May it be lightweight implementations or like my current
use-case webservice only controllers that route all their actions
through soap, xml-rpc or a rest server. I would really appreciate if
more people would vote +1 on this issue to get it included in 1.7

In the last weeks i also played around with
`CouchDb <http://incubator.apache.org/couchdb/docs/overview.html>`_, a
document based database. Its the perfect storage medium for blogs, wikis
or other knowledge-based applications and comes with a lightweight and
easy REST Api for ClientSide access. Within the
`Zym <http://www.zym-project.com>`_ project i managed to implement a
prototype that is based on Jurrien's prototype for a CouchDb client.
`Matthew of Zend Fame published a proposal for a Zend
Couch <http://framework.zend.com/wiki/display/ZFPROP/Zend_Couch+-+Matthew+Weier+O'Phinney>`_
component yesterday and we teamed up to implement two prototypes
(`mine <http://github.com/weierophinney/phly/tree/beberlei>`_ is based
on `Matthews <http://github.com/weierophinney/phly/tree/master>`_ and
integrates lots of stuff of the Zym component).



.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>