Using Assertions for validation
===============================

We all know PHP is weakly typed and has some weird type-conversion rules.
This can often complicate our code checking for invalid or illegal data.
Using if/else clauses we can do all sorts of validation, but with standard
coding styles (PSR, Zend, PEAR) we end up with at least 3 lines per check,
cluttering the whole code-base.

Take `this example
<http://phpazure.codeplex.com/SourceControl/changeset/view/67037#840935>`_ from
the old deprecated Windows Azure SDK, a method for putting a binary file into
Azures blob storage:

.. code-block:: php

    <?php
    public function putBlob($containerName = '', $blobName = '', $localFileName = '', $metadata = array(), $leaseId = null, $additionalHeaders = array())
    {
        if ($containerName === '') {
            throw new Microsoft_WindowsAzure_Exception('Container name is not specified.');
        }
        if (!self::isValidContainerName($containerName)) {
            throw new Microsoft_WindowsAzure_Exception('Container name does not adhere to container naming conventions. See http://msdn.microsoft.com/en-us/library/dd135715.aspx for more information.');
        }
        if ($blobName === '') {
            throw new Microsoft_WindowsAzure_Exception('Blob name is not specified.');
        }
        if ($localFileName === '') {
            throw new Microsoft_WindowsAzure_Exception('Local file name is not specified.');
        }
        if (!file_exists($localFileName)) {
            throw new Microsoft_WindowsAzure_Exception('Local file not found.');
        }
        if ($containerName === '$root' && strpos($blobName, '/') !== false) {
            throw new Microsoft_WindowsAzure_Exception('Blobs stored in the root container can not have a name containing a forward slash (/).');
        }
        // rest of the code here
    }

The rest of this components public API methods look about the same. It is a
very complete validation of the input data, however its not very readable.
Instead you have 6 if branches, which increase the complexity of the method
and almost take up half the screen without even getting to the actual code.

The assertion pattern is really helpful here to reduce the complexity of this
code and hide the ``if/throw`` conditions into little helper methods. Have a
look at a refactored method using my `Assert
<https://github.com/beberlei/assert>`_ micro-library.

.. code-block:: php

    <?php
    public function putBlob($containerName = '', $blobName = '', $localFileName = '', $metadata = array(), $leaseId = null, $additionalHeaders = array())
    {
        Assertion::notEmpty($containerName, 'Container name is not specified');
        self::assertValidContainerName($containerName);
        Assertion::notEmpty($blobName, 'Blob name is not specified.');
        Assertion::notEmpty($localFileName, 'Local file name is not specified.');
        Assertion::file($localFileName, 'Local file name is not specified.');
        self::assertValidRootContainerBlobName($containerName, $blobName);

        // rest of the code
    }

This is much more readable, using two custom assertions and some general
assertions.

There is one risk here though, you introduce additional coupling to another
library/namespace. Especially when you start using this pattern on a large
scale, you have to make sure this assertions are **VERY** stable and
unit-tested.

That is why you should extend from ``Assertion`` and use your own class when
using the Assert library. This returns some control in your hands and even
allows you to overwrite the exception class:

.. code-block:: php

    <?php
    namespace MyProject\Util;

    use Assert\Assertion as BaseAssertion;

    class Assertion extends BaseAssertion
    {
        static protected $exceptionClass = 'MyProject\Util\AssertionFailedException';
    }


.. author:: default
.. categories:: PHP
.. tags:: AssertLibrary
.. comments::
