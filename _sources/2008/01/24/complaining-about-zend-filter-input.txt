Complaining about Zend_Filter_Input
===================================

Zend\_Filter\_Input is really nice to be sure form data is filtered
correctly, but i have some serious complaints: Why the hell are the
error messages so user-unfriendly? I really would like to use the output
of Zend\_Filter\_Input::getMessages(), but I could never trust to show
them to a user of my website: They are obviously written for developers.
Some examples:

    '' does not appear to be an integer '' is an empty string

I use a ton of validators to filter the comments form and all possible
error messages that can be thrown are not "user-save". Because all these
messages are handled in each Validator class its almost impossible to
change them without going nuts:

.. code-block:: php

    $validators = array(
        'article_id' => array(
            'Int',
            new Zend_Validate_Int(),
            array('GreaterThan', 0)
            ),
        'username' => 'Alnum',
        'userEmail' => new Zend_Validate_EmailAddress(Zend_Validate_Hostname::ALLOW_DNS | Zend_Validate_Hostname::ALLOW_LOCAL, true),
        'cp'   => array(
            'Digits',                // string
            new Zend_Validate_Int(), // object instance
            array('Between', 1138, 1138)  // string with constructor arguments
        ),
        'comment' => 'NotEmpty',
    );

This simple $validators requirement creates templates for error
messages in each validator object, that are: Zend\_Validate\_Int,
Zend\_Validate\_Alnum, Zend\_Validate\_EmailAddress,
Zend\_Validate\_Hostname, and the not empty message. To allow for user
friendly messages one had to make child objects of each of the
Validators and edit the error messages accordingly. I avoid this by
printing my own errors from outside the Zend\_Filter\_Input, rather than
using the object for what it is probably supposed to do.

.. categories:: none
.. tags:: ZendFramework
.. comments::
