Why does the PHP extension fail to load with _zval_ptr_dtor_wrapper error
=========================================================================

I sometimes come across this error when loading an extension in PHP

::

    PHP Warning:  PHP Startup: Unable to load dynamic library
    '/usr/lib64/php-zts/5.5/modules/myext.so' -
    /usr/lib64/php-zts/5.5/modules/myext.so: undefined symbol:
    _zval_ptr_dtor_wrapper in Unknown on line 0

From the Google results it is not very easy to find out what this means.

Technically the extension was compiled with a PHP version using the
``-enable-debug`` flag, which wraps all calls to ``zval_ptr_dtor`` in a wrapper
macro that does not exist in a regular, non-debug build.

But a debug extension and non-debug PHP are incompatible.

PHP extensions are only compatible between different installations if the
following constraints are the same for the compiling and the executing PHP
binary:

- OS (Linux, Mac)
- libc (glibc or musl for Alpine)
- PHP version up to the minor level (5.5, 5.6, 7.0, 7.1)
- extension version (20151012 for PHP 7.0)
- thread-safety (ZTS) or non-thread-safety (NTS)
- debug or non-debug (``--enable-debug`` flag during compile).


.. author:: default
.. categories:: none
.. tags:: PHPExtension
.. comments::
