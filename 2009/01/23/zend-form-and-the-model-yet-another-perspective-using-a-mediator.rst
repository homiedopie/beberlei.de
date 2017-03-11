Zend_Form and the Model: Yet another perspective using a Mediator
=================================================================

`Matthew Weier O'Phinney <http://weierophinney.net/matthew/>`_ of the
Zend Framework Devteam `wrote a controversial post on integrating
Zend\_Form and the Model last
month <http://weierophinney.net/matthew/archives/200-Using-Zend_Form-in-Your-Models.html>`_.
He separated concerns of view and model that communicate via a Form, by
calling just thee validation functions on the Form inside the mode. On
request you could retrieve the model to the controller and view layers.
I already wrote into his comments that I didn't like the solution
because it relies on implicit rules for the developers to use the Form
component correctly in all layers. Additionally the building of the form
using this approach would be performed inside the model, although
strictly speaking this is responsibility of the View Layer. Another
negative point is duplication of input filtering code that has to be
performed to use certain variables inside the controller or when
different forms talk with the same model.

`Jani <http://codeutopia.net>`_ took it up and `proposed writing
validators for forms and attaching them to the
Form <http://codeutopia.net/blog/2009/01/07/another-idea-for-using-models-with-forms/>`_
as sort of a mediator. I am not a fan of this approach either, because
the validator would have to include domain logic but is not really a
part of the domain logic anymore but just a validator. Developers might
forget using the validator inside the model for all their actions or
there would be duplication of code in some places. In a perfect world,
only functions of the models public interface should be called for
validation.

My personal favorite for Form and Model integration is a **mediator**
object between the two layers. Your model will have to include an
additional interface with one function **acceptFormRequest($values);**
which accepts an array of validated Zend Form field values. It then
tries to apply the validated data into a record. Additional required
validations of the model can take place in this function, which
separates the concerns of Form validation and Model data validation.
Still the mediator merges those differences together: You can throw an
Exception and it will be attached as a custom error message to the Form.
The following very short code will show the required interface and the
mediator code. This code is very simple and might produce maintenance
overhead fast, but I propose some refactoring enhancements later in the
discussion.

    ::

        interface WW_Model_AcceptFormRequest
        {
            /**
             * Acceept a form request
             * @param array $values
             * @return WW_Record_Interface
             */
            public function acceptFormRequest($values);
        }
        class WW_Model_FormMediator
        {
            /**
             * Try to push the form request to the model
             * 
             * @param Zend_Form $form
             * @param WW_Model_AcceptFormRequest $model
             * @return WW_Record_Interface
             */
            public function pushFormToModel(Zend_Form $form, WW_Model_AcceptFormRequest $model)
            {
                if(!$form->isValid()) {
                    throw new Exception("Form not valid!");
                } else {
                    $values = $form->getValues();
                    try {
                        $record = $model->acceptFormRequest($values);
                    } catch(Exception $e) {
                        // This exception message comes from the model, because validation failed
                        $form->addErrorMessage($e->getMessage());
                        throw new Exception("Form request not accepted by model!");
                    }
                }
                return $record;
            }
        }

You can see the mediator has two different stages where errors can
occur: When the form is not valid or the model is not valid. Both exits
can be catched inside the controller and are the indicator that the form
has to be displayed again for further input corrections. When successful
the model returns a valid record that applies to the form and model
requirements and can be displayed. If this record should be persistent
this would have been done inside the **acceptFormRequest** function
already. An example using a very simple Model using the a BankAccount
example. We have a form that validates all the incoming request data for
a withdrawal of money, though does not validate it against the models
internal state. Our BankAccountModel implements the
**WW\_Model\_AcceptFormRequest** interface and returns a valid
BankAccount. If found the given amount is withdrawn.

    ::

        class BankAccountModel implements WW_Model_AcceptFormRequest {
            public function acceptFormRequest($values)
            {
                $bankAccount = $this->getBankAccountBy($values['bankAccountNumber'], $values['pin']);
                if($values['action'] == "withdraw") {
                    $bankAccount->withdraw($values['amount']);
                    $this->save($bankAccount);
                } else {
                    // unknown action...
                }
            }
            public function getBankAccountBy($key, $password) {
                // Find by Primary Key returning 'BankAccount' instance or exception if not found.
            }
            public function save(BankAccount $ba) {
                // Sql for saving the Bank Account
            }
        }

        class BankAccount
        {
            public function withdraw($amount)
            {
                if( ($this->getBalance()-$amount) < 0 ) {
                    throw new Exception("You cannot withdraw more money than your bank account holds!");
                }
                $this->balance -= $amount;
            }
        }

Two exceptions might be thrown in this case: The Bank Account number
does not exist or the password is wrong. Or you are not allowed to
withdraw the given amount of money. If any of those exceptions is thrown
the Model does not accept the form data and the form will have to be
displayed again for the client showing the new error message that was
returned from the model. The controller handling this process would look
like this:

    ::

        class BankAccountController extends Zend_Controller_Action {
            public function performWithdrawlAction() {
                $form = new BankAccountWithdrawlForm(); // extends Zend_Form and builds the form

                if($this->getRequest()->isPost()) {
                    $mediator         = new WW_Model_FormMediator();
                    $bankAccountModel = new BankAccountModel();
                    try {
                        $bankAccount = $mediator->pushFormToModel($form, $bankAccountModel);

                        $this->view->assign('bankAccount', $bankAccount); // Show new balance in view!
                    } catch(Exception $e) {
                        $this->view->assign('withdrawlForm', $form);
                        $this->_redirect('showWithdrawl');
                    }
                } else {
                    $this->view->assign('withdrawlForm', $form);
                    $this->_redirect('showWithdrawl');
                }
            }
        }

You can see the mediator tightly integrates Form and Model without both
components knowing too much of each other. Still you can add error
messages received from the model into the Form and redisplay it. One
negative point of this approach is the fact that you only have one
method for accepting form data, which could result in variable checking
and redispatching in the case of many different operations that can be
performed on the same model. For this case you might want to either:

#. Rewrite the mediator to accept a specific model class (not the
   interface) and call the required custom method that matches the forms
   request. (Best approach for separation concerns)
#. Rewrite the mediator to also pass the **get\_class($form);** value to
   the model for decision making (Faster approach)

There is still some overhead on using the mediator. Since its generic
you could build an Action Helper for it and use the direct call
mechanism to save some lines of code.

.. categories:: none
.. tags:: ZendFramework
.. comments::
