
Implementing Zend Auth, Acl and Caching
=======================================

I managed to work a bit on the blog, enabling me to have new instance in
the series, How to refactor and extend your own blog software using
`Zend Framework <http://framework.zend.com>`_. This time: Implementing
meaningful Auth and ACL mechanisms and `fixing view
caching <http://www.whitewashing.de/blog/articles/41>`_, which did not
work in its original implementation due to different users groups
sharing the same cached views.

In the last days I came across two in depth tutorials on Zend\_Acl and
Zend\_Auth integration to MVC. Most people propably saw the DevZone
article "`Zend\_Acl and MVC Integration (part
1) <http://devzone.zend.com/article/3509-Zend_Acl-and-MVC-Integration-Part-I-Basic-Use>`_"
by Aldemar Bernal on the Frameworks Frontpage. Another good article was
written by Frank Ruske in the latest german `PHP
Magazin <http://www.phpmagazin.de>`_ (`Zipped Source Code of the
Example <http://it-republik.de/zonen/magazine/ausgaben/psfile/source_file/14/Seite_80__482a98c572a5c.zip>`_).
I took the best ideas of both articles and merged them into the existing
components of my blog.

This now enables me to cache the site depending on the Auth status of
the page user agent. The blog is now caching all views that are
generated for guest users. Since there is no "registered" or "member"
account yet, this means the blogs content is cached and served from
cache for everyone except me when I am logged in. To get this work I
added some simple additional check in `Matthews Cache View Controller
Plugin <http://devzone.zend.com/article/3372-Front-Controller-Plugins-in-Zend-Framework>`_:

    ::

        public function dispatchLoopStartup(Zend_Controller_Request_Abstract $request)
        {
            $auth = Zend_Auth::getInstance();
            if($auth->hasIdentity()) {
                self::$doNotCache = true;
                return;   
            }
            [..]
        }

This prevents caching for registered identities.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>