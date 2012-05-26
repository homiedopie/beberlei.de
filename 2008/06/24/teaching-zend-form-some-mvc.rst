
Teaching Zend_Form some MVC
===========================

Lots of people complain that Zend Form runs counter to the MVC spirit,
because it handles validation, business logic and view elements all in
one acting as Model, Controller and View.

Extending the Zend Form component to handle all this different aspects
in different layers of the application is rather easy though. What we
want of a MVC compatible Form object is the following:

-  The **model** escapes and validates all the data that is put into the
   form.
-  The **view** decides on how the form is displayed.
-  The **controller** moves data from the model to the view and back,
   handling the stages of the form request.

The first step is, **allowing any Model that implements
Zend\_Validator\_Interface to hook into the Zend\_Form Validation
process**. We generate a new class, WW\_Form\_Mvc and allow a function
setModel() to insert any Model object that implements
Zend\_Validator\_Interface into the form. We extend isValid(),
getMessages() and getErrors() to not only check all the form elements
validators, but also the models validators. Please note that the
array\_merge() solution is not the correct way of how this snippet
should work. Any merge operation of the messages and errors has to be on
a field key level, which is not currently done.

    ::

        class WW_Form_Mvc extends Zend_Form
        {
            protected $model = null;
            
            /**
             * Extends isValid() method of Zend Form to check for validity of specified model
             * @param Array $data
             * @return Boolean
             */
            public function isValid($data)
            {
                $valid = parent::isValid($data);

                if($valid == true && !is_null($model)) {
                    $valid = $this->model->isValid($data) && $valid;
                }
                return $valid;
            }
            
            /**
             * Extends getMessages() Validator Interface implementation of Zend Form to also
             * return the messages of the Model validation.
             * @return Array
             */
            public function getMessages($name = null, $suppressArrayNotation = false)
            {
                $messages = parent::getMessages($name, $suppressArrayNotation);
                
                if(!is_null($model)) {
                     $form_messages = $this->model->getMessages();

                     $messages = array_merge($messages, $form_messages);
                }
                
                return $messages;
            }
            
            /**
             * Extends getErrors() Validator Interface implementation of Zend Form to also
             * return the errors of the Model validation.
             * @return Array
             */
            public function getErrors($name = null)
            {
                 $messages = parent::getErrors($name);

                if(!is_null($model)) {
                     $form_messages = $this->model->getErrors();

                     $messages = array_merge($messages, $form_messages);
                }
                
                return $messages;
            }
            
            /**
             * Set a Model object, which has to implement Zend_Validate_Interface
             * @throws Zend_Exception
             */
            public function setModel($model)
            {
                if($model instanceof Zend_Validate_Interface) {
                    $this->model = $model;
                } else {
                     throw new Zend_Exception('WW_Form_Mvc expects a model of type Zend_Validate_Interface');   
                }
            }
        }

    We then extend the WW\_Form\_Mvc class to disable the automatic
    loading of decorators in the Constructor and additionally allow to
    pass a Model to the constructor as second argument:

        ::

            class WW_Form_Mvc
            {
                protected $model = null;

                /**
                 * this overrides the original Zend_Form Constructor and skips
                 * the decorator initilisation, because this is now being handled
                 * by View Helpers
                 */
                public function __construct($options=null, $model=null)
                {
                    if (is_array($options)) {
                        $this->setOptions($options);
                    } elseif ($options instanceof Zend_Config) {
                        $this->setConfig($options);
                    }

                    // Extensions...
                    $this->init();   
                    
                    if(!is_null($model)) {
                         $this->setModel($model);   
                    }
                }

                // All the other stuff here
            }

    In our views we want to **use helper methods to manage the
    displaying of the form**. For each different style of form
    displaying, we can generate different helpers. For example a helper
    that would only apply the default decorators would look like this:

        ::

            class WW_View_Helper_FormDefault
            {
                /**
                 * Load only default decorators on this Zend_Form object
                 *
                 * @param Zend_Form $form
                 */
                public function formDefault(Zend_Form $form)
                {
                    if($form instanceof Zend_Form) {
                        $form->loadDefaultDecorators();
                        return $form;
                    }
                }
            }

    We can now use this helper and in any template say: <?=
    $this->formDefault($this->someForm); ?> We can now look at our
    controller action that implements this form and we will see that it
    does not look different from what we would have done before:

        ::

            function formAction()
            {
                $model = new SomeModel();

                $form = new WW_Form_Mvc();
                $form->setModel($model);

                // generate form here, adding elements and stuff

                if($form->isValid($_POST)) {
                    $model->insert($form->getValues());
                    $this->view->form = "Form was submitted!";
                } else {
                    $this->view->form = $form;
                }
            }

    Isnt that nice? Now each part of the equation is doing what its
    supposed to do.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>