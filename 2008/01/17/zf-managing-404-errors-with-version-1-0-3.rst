ZF: Managing 404 Errors with Version 1.0.3
==========================================

Ok, the description of the Link referring to the `version 0.9 solution
for Managing 404
errors <http://www.bigroom.co.uk/blog/managing-404-errors-in-the-zend-framework>`_
due to missing modules or actions is wrong. It is not enought to replace
Zend::loadClass with Zend\_Loader::loadClass. Other functions have been
renamed, my current snippet is:

.. code-block:: php

    /**
     * Original Snippet from: http://www.bigroom.co.uk/blog/managing-404-errors-in-the-zend-framework
     */
        class NoroutePlugin extends Zend_Controller_Plugin_Abstract
        {
            public function preDispatch(Zend_Controller_Request_Abstract $request )
            {
                $dispatcher = Zend_Controller_Front::getInstance()->getDispatcher();

                $controllerName = $request->getControllerName();
                if (empty($controllerName)) {
                    $controllerName = $dispatcher->getDefaultControllerClass($request);
                }
                $className = $dispatcher->formatControllerName($controllerName);
                if ($className)
                {
                    try
                    {
                        // if this fails, an exception will be thrown and
                        // caught below, indicating that the class can't
                        // be loaded.
                        Zend_Loader::loadClass($className, $dispatcher->getControllerDirectory());
                        $actionName = $request->getActionName();
                        if (empty($actionName)) {
                            $actionName = $dispatcher->getDefaultAction();
                        }
                        $methodName = $dispatcher->formatActionName($actionName);

                        $class = new ReflectionClass( $className );
                        if( $class->hasMethod( $methodName ) )
                        {
                            // all is well - exit now
                            return;
                        }
                    }
                    catch (Zend_Exception $e)
                    {
                        // Couldn't load the class. No need to act yet,
                        // just catch the exception and fall out of the
                        // if
                    }
                }

                // we only arrive here if can't find controller or action
                $request->setControllerName( 'blog' );
                $request->setActionName( 'noroute' );
                $request->setDispatched( false );
            }
        }

I hope someone needs this as much as me.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>
