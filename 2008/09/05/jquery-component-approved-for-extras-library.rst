.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

jQuery Component approved for extras library
============================================

Yesterday both my jQuery Helper proposals (`Core
Helper <http://framework.zend.com/wiki/display/ZFPROP/ZendX_JQuery_View_Helper_JQuery+-+Benjamin+Eberlei>`_,
`UI
Widgets <http://framework.zend.com/wiki/display/ZFPROP/ZendX_JQuery+UI+Widgets+Extension+-+Benjamin+Eberlei?focusedCommentId=7373203#comment-7373203>`_)
for the Zend Framework have been accepted for development. I have
already checked my working prototypes `into the Zend Framework
SVN <http://framework.zend.com/svn/framework/extras/incubator/>`_. In my
opinion the usage is quite stable already. There is likely to be no
argument flip, function renaming or whatsoever. I have renamed the
jqLink helper to ajaxLink though, because other libraries are offering
the same functionality to make Ajax related calls and this way the
learning curve for people using different libraries in different
projects may be more easy.

What is still missing? I have to add captureStart()/captureEnd()
functions to the Container Widgets Accordion and Tabs, and will create
additional pane helpers for both of them. This will likely be finished
this weekend and then there is only the documentation missing. I am very
confident this component will be finished for the Zend Framework 1.7
release later this year.

Since this component also includes helpers for the jQuery UI Widgets 1.6
release (which is not released yet), a little waiting time before
release is still good. I hope this all works out and the jQuery UI 1.6
release is in the Google CDN, when ZF 1.7 comes out.
