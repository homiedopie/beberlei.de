:author: beberlei <kontakt@beberlei.de>
:date: 2008-06-21

Simplifying ZF: Scope of Variables in View and Controller
=========================================================

As a follow up on the `Zend Framework, "Web 2.0 Framework" My
Ass! <http://destiney.com/blog/zend-framework-web-2-0-framework-my-ass>`_
article referend earlier I came up with some simplifications of the Zend
View and Controller variable coupling.

Using some code in the article I created a new Zend\_View\_Extended
class which offers the possibility to circumvent the access of variables
via $this and directly registers each variable key of the Zend\_View
object as an own variable in the script template:

    ::

        class Zend_View_Extended extends Zend_View_Abstract
        {
            protected function _run()
            {
                while( list( $k, $v ) = each( $this ) ) ${$k} = $v;

                include func_get_arg(0); 
            }
        }

Now rather than calling $this->data you can call $data in a script
template. Of course this comes with additional overhead of each variable
being registered twice. I dont know how this handles performance wise,
but maybe unsetting $this variables after copying solves this. Also you
have to overwrite the initView() method of your base Controller Action
class.

Another simplyfication would be to allow for the following direct
variable settings in any Controller Action, which would shorten the
$this->view->variable call, to derive the same functionality via
$this->variable. I haven't tested this though.

    ::

        class Zend_Controller_SimpleAction extends Zend_Controller_Action
        {
            function __set($name, $value)
            {
                $this->view->{$name} = $value;
            }
        }

