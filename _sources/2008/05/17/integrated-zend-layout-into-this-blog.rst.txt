Integrated Zend_Layout into this blog
=====================================

I finished with integrating Zend\_Layout into this blog software today.
At first I thought it is quite hard to use especially if you want to
integrate dynamic navigational contents depending on the current
module/controller/action setup. But I came up with a combination of
actionStack and Named Response Sections as `described in the ZF
Documentation of the Layout
component <http://framework.zend.com/manual/en/zend.layout.quickstart.html#zend.layout.quickstart.mvc>`_,
which is quite easy to understand, use and extend.

At each of the major Controllers I put different actions from a specific
Navigation Controller on the
`ActionStack <http://framework.zend.com/manual/en/zend.controller.actionhelpers.html#zend.controller.actionhelpers.actionstack>`_
(mostly global per Controller using the init() class method).

A typical controller looks like this:

    ::

        class BlogController extends Zend_Controller_Action
        {
            public function init()
            {            
                $this->_helper->actionStack('tagcloud', 'Navigation');
                $this->_helper->actionStack('userinfo', 'Navigation');
            }
        }

The NavigationController looks like this:

    ::

        class NavigationController extends Zend_Controller_Action
        {
            public function tagcloudAction()
            {
                // Do not render the content of this action to the default output.
                $this->getHelper("ViewRenderer")->setNoRender();

                [...]

                // Append content to secondaryNavigation named response section
                $this->getResponse()->append('secondaryNavigation', $this->view->render('navigation/tagcloud.phtml'));
            }
        }

The layout.pthml then just calls certain named sections, for example <=?
$this->layout()->secondaryNavigation; ?>

.. categories:: none
.. tags:: ZendFramework
.. comments::
