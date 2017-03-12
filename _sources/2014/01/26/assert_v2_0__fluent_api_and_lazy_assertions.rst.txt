Assert v2.0: Fluent API and Lazy Assertions
===========================================

Almost two years ago I started developing a small library `Assert
<https://github.com/beberlei/assert>`_ (`blog post
<http://www.whitewashing.de/2012/09/04/using_assertions_for_validation.html>`_)
which contained a set of assertion methods to use in production code. With
18.000 installations from Packagist this is my most successful piece of open
source software outside of the Doctrine universe. There is a fair number
of contributors and I know several companies using the library in production.

The API however didn't make me too happy, using the static method calls
made it impossible to collect multiple errors and also made the code
more verbose than necessary when validating the same value with multiple
assertions.

Several weeks ago I stumbled across the Java library `AssertJ
<http://joel-costigliola.github.io/assertj/>`_ that gave me the idea how to fix
these problems. The last two days I had some time to implement those new
functionalities and I am releasing a new version 2.0 of Assert today.

Fluent API
----------

Instead of having to use the static assertion methods, there is now
a new fluent API, invoked by calling the function ``Assert\that($value)``
and then all the assertions you want to call on that value.

Here are some examples:

.. code-block:: php

    <?php

    \Assert\that(10)->notBlank()->integer()->range(0, 100);
    \Assert\that(array('foo', 'bar'))->isArray()->all()->string();
    \Assert\that(null)->nullOr()->boolean();

This new API allows for much shorter and compact assertions.

Lazy Assertions
---------------

Using Assert with webforms was never possible unless you wanted to show
the user only exactly one error message. Because every assertion fails
with an Exception, there was no way to execute multiple assertions and
collect the errors. This has changed with the new lazy assertion API,
that is similar to the Fluent API:

.. code-block:: php

    <?php
    \Assert\lazy()
        ->that(10, 'foo')->string()
        ->that(null, 'bar')->notEmpty()
        ->that('string', 'baz')->isArray()
        ->verifyNow();

The method ``that($value, $propertyPath)`` requires a property path (name), so
that you know how to differentiate the errors afterwards.

On failure ``verifyNow()`` will throw an exception
``Assert\\LazyAssertionException`` (this does not extend
``AssertionFailedException``) with a combined message:

::

    The following 3 assertions failed:
    1) foo: Value "10" expected to be string, type integer given.
    2) bar: Value "<NULL>" is empty, but non empty value was expected.
    3) baz: Value "string" is not an array.

You can also call the method ``getErrorExceptions()`` to retrieve all the
underyling ``AssertionFailedException`` objects and convert them something
useable for the frontend.

Error Messages, Values and Constraints
--------------------------------------

In version 1.0 Assert did not have default error messages when failures
occured. This has changed and now every assertion has a default failure
message, as well as access to the value and constraints of an exception:

.. code-block:: php

    <?php

    use Assert\AssertionFailedException;

    try {
        \Assert\that(10)->range(100, 1000);
    } catch (AssertionFailedException $e) {
        $e->getMessage(); // Value "10" is not between 100 and 1000.
        $e->getValue(); // 10
        $e->getConstraints(); // array('min' => 100, 'max' => 1000)
    }

This helps during development when the assertion exceptions occur and also
allows to provide error messages to the user, by using the exception code and
the value and constraint data for translating into human readable messages.

You can find more information in the `README of Assert
<https://github.com/beberlei/assert#assert>`_.

.. author:: default
.. categories:: PHP
.. tags:: AssertLibrary
.. comments::
