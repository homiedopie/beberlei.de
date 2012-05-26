.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Test your Legacy PHP Application with Function Mocks!
=====================================================

Much talking is going on about Unittesting, Mocks and TDD in the PHP
world. For the most this discussions surround object-oriented PHP code,
frameworks and applications.

Yet I would assert that the reality for PHP developers (me included) is
dealing with PHP 4, PHP 5 migrated, or non-object oriented legacy
applications which are near to impossible to bring under test. Still
this code works, is in production and needs maintenance and possibly
extension for new features.

For example many applications may still use **mysql\_\*** functions at
length inside their model or have multiple nested function levels
(Example: Wordpress). `Runkit <http://pecl.php.net/package/runkit>`_ to
the rescue: A PECL extension that can hack your running PHP code, such
that method or functions are repointed to execute new implementations.
Using this extension you can actually mock out internal PHP functions,
which is great to bring legacy code under test.

Consider this following proof of concept, `using the Runkit extension
build by Padraic Brady <http://github.com/padraic/runkit/tree/master>`_
(the one from pecl.php.net does not compile on PHP 5.2), which replaces
the functionality of **mysql\_query()**. You have to set the following
option in your php.ini: **runkit.internal\_override = On** for this to
work. By default only user-defined functions may be overwritten by
Runkit.

    ::

        class FunctionMocker
        {
            protected $_mockedFuncBehaviourMap = array();

            public function mock($funcName, $return=null)
            {
                $newFuncCode = 'return "'.$return.'";';
            
                $renamedName = "__".$funcName."_mockOriginalCopy";
                runkit_function_copy($funcName, $renamedName);
                runkit_function_redefine($funcName, '', $newFuncCode);
                
                $this->_mockedFuncBehaviourMap[$funcName] = $renamedName;
            }
            
            public function reset()
            {
                foreach($this->_mockedFuncBehaviourMap AS $funcName => $renamedName) {
                    runkit_function_remove($funcName);
                    runkit_function_copy($renamedName, $funcName);
                    runkit_function_remove($renamedName);
                }
                $this->_mockedFuncBehaviourMap = array();
            }
        }

        $mocker = new FunctionMocker();
        $mocker->mock('mysql_query', 'hello world!');

        echo mysql_query(); // hello world

        $mocker->reset();

        mysql_query(); // error

    This example, only allows for string return values of the mock and
    has no support for replacing the arguments of the mocked function.
    Also chaining of different return values based on input or call
    number might be interesting. Some kind of Code Generator Tool would
    have to be implemented to support this functionality. Additionally
    Assertions and Verifying should be implemented for the function
    arguments. All in all this would allow to mock functions as you
    would mock interfaces/classes, which would be a great addition for
    all those legacy applications that use procedural PHP.

    Additionally what the real killer for runkit would be: The
    possibility to insert PHP callbacks instead of real PHP code into
    the **runkit\_function\_redefine**.
