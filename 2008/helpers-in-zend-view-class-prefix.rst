:author: beberlei <kontakt@beberlei.de>
:date: 2008-01-14

Helpers in Zend_View: Class Prefix
==================================

I have to say, the Zend Framework documentation is a bit imprecise
sometimes. Regarding custom Helpers in Zend\_View it states:
    The class name must, at the very minimum, end with the helper name
    itself, using CamelCaps. E.g., if you were writing a helper called
    "specialPurpose", the class name would minimally need to be
    "SpecialPurpose". You may, and should, give the class name a prefix,
    and it is recommended that you use 'View\_Helper' as part of that
    prefix: "My\_View\_Helper\_SpecialPurpose". (You will need to pass
    in the prefix, with or without the trailing underscore, to
    addHelperPath() or setHelperPath()).

What does that mean regarding how your Helper has to be called? The
default prefix for a Helper function that should be called foobar() is
actually:
    ::

        class Zend_View_Helper_Foobar()
        {
            function foobar() { }
        }

It took me some time to realize that. Why doesn't Zend just give an
example like that? To change the prefix in a context of the
Zend\_Controller\_Action you have to do something like this:
    ::

        class SomeController extends Zend_Controller_Action
        {
            function init() {
                $this->initView();
                $this->view->addHelperPath("pathtohelpers", "ClassPrefix");
            }
        }

