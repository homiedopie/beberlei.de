Porting Extension to PHP7
=========================

This blog post might be weird to read, but in it I am documenting how I ported
our `Tideways PHP Profiler
<https://github.com/tideways/php-profiler-extension>`_ from a PHP5 to PHP7
extension, step by step. This could act as a reference to others, having to
port extensions themselves.

The starting point is the `PHPNG-Upgrading
<https://wiki.php.net/phpng-upgrading>`_ wiki page, which is slighty outdated -
but I am doing my best to put everything I stumbled on in there.

First, I started doing a port that does **not** run on both PHP5 and PHP7 to
get familiar with the potential changes.

1. macro "zend_hash_update" passed 6 arguments, but takes just 3

This is the start of changes to the ``zend_hash_*`` family of functions that
instead of a char and its length for a key, no accept ``zend_string``.

I started with this one because it was responsible for almost half of the
errors, but I realized soon that you need to start with ``zend_string``
in PHP 7.

2. Discussing in ``#gophp7-ext`` IRC channel about approach

When i realized that the extension has a ``hp_string`` abstraction for PHP5
already and it looked similar to the PHP7 ``zend_string`` i started getting
curious about approaches from others.

`Derick <http://derickrethans.nl/>`_ was optimistic that you could have one
branch for both PHP5 and PHP7 support and `Guilherme
<https://twitter.com/guilhermeblanco>`_ linked me two patches from `libsodium
<https://github.com/jedisct1/libsodium-php/pull/23/files#diff-0f29a49441e3d73202e3abaab7c324b0R73>`_
and `php-mustache
<https://github.com/jbboehr/php-mustache/pull/11/files#diff-7905585bdfbda727fb2f2554f4d8a913R13>`_ shimming the string API for php5.

The libsodium approach looked cleaner so I reverted my previous hash changes
and started over.

3. Introducing a zend_string shim for PHP5

I introduced their conditional ``zend_string`` definition and started to
replace my ``hp_string`` implementation with it and get it to compile on PHP
5.6:

- Every ``hp_create_string(const char *value, int len)`` is replaced with
  ``zend_string_init(const char *value, size_t len, int persistent)``.

- Every ``hp_zval_to_string()`` is replaced with the ``Z_STR_P()`` macro.
  The occurance of ``hp_string_to_zval()`` is replaced with a compatibility
  macro ``RETURN_STR_COPY``.

- Every ``hp_clean_string()`` is replaced with the function ``zend_string_release()``.

I got stuck for some time with the ``size_t len`` in the init function, because
I passed the the size (+1).

The resulting commit 4da8e0a actually removes more code, because I could get
rid of my ``hp_string`` struct and the corresponding code.

4. Introducing shims for string length and long in zend parameter API

PHP7 changes ``zend_parse_parameters`` to return a ``size_t`` instead of an
``int`` for a char and ``zend_long`` instead of ``long`` for a long.
The following conditional typedefs help with that:

.. code-block:: c

    #if PHP_MAJOR_VERSION < 7
    typedef long zend_long;
    typedef int strsize_t;
    #else
    typedef size_t strsize_t;
    #endif

I then needed to exchange all occurances for ``long`` and ``int`` in php
functions.

Commit 163c743ca8f2706a40420194294683458a9973f9 has the juicy details.

5. Porting ``zend_execute_data`` (I): Arguments and Object Pointer

If you have worked with overwriting the ``zend_execute`` and ``zend_execute_internal`` hooks before
then you know that even during PHP5 it already is a big macro if/elif/else block. Again the
``zend_execute_data`` struct has changed considerably, so I started porting it:

First, ``data->function_state.arguments`` was removed and replaced with a pair
of macros ``ZEND_CALL_NUM_ARGS`` and ``ZEND_CALL_ARG``. Loosing access to all
arguments I was forced to redesign the callback API and pass
``zend_execute_data`` down to each callback.

See commit 1e46869 for the compatibility layer with the argument access.

6. Porting ``zend_execute_data`` (I): Function Names

The Profiler extension needs the class qualified name of a function call.
This change was straight forward, all the chars inside zend_execute_data
are now zend_strings and need to be handled accordingly.

7. Porting ``zend_execute`` and ``zend_execute_internal`` calback

Again, slight changes in the callbacks need to be handled with #if/#else.

See commit bfd0ff9702e3ebfd2ae2fb0d5556971fbeda4fc6

8. Struct ``zend_call_info`` changes

Now that PHP doesn't use so many zval pointers and pointer-pointers anymore
we have to make slight adjustments to ``zend_call_info``:

.. code-block:: c

    #if PHP_MAJOR_VERSION < 7
        twcb->fci.retval_ptr_ptr = &retval;
    #else
        twcb->fci.retval = retval;
    #endif

See commit da60ceb115887e278bec1013a90d6a6e417abe2c for more details.

At this point I am only down from 187 compiler errors to 172, the following
ones are missing:

::

    1    add_assoc_string_ex(return_value, "message", sizeof("message"), PG(last_error_message), 1);
    1  'add_assoc_stringl' undeclared (first use in this function)
    1  'curr_func' undeclared (first use in this function)
    1  incompatible type for argument 1 of 'zval_addref_p'
    8  incompatible types when initializing type 'struct zval *' using type 'zval'
    1  invalid type argument of unary '*' (have 'zval')
    1  macro "add_assoc_stringl" passed 5 arguments, but takes just 4
    1  macro "RETURN_STRING" passed 2 arguments, but takes just 1
    1  macro "zend_hash_get_current_data" passed 2 arguments, but takes just 1
    1  macro "zend_hash_index_update" passed 5 arguments, but takes just 3
    1  macro "zend_hash_merge" passed 6 arguments, but takes just 4
    90  macro "zend_hash_update" passed 6 arguments, but takes just 3
    5  macro "ZVAL_STRING" passed 3 arguments, but takes just 2
    1  'RETURN_STRING' undeclared (first use in this function)
    1  too few arguments to function '_zend_execute_internal'
    4  too few arguments to function 'zend_read_property'
    4  too many arguments to function 'add_assoc_string_ex'
    1  too many arguments to function 'pcre_get_compiled_regex_cache'
    14  too many arguments to function 'zend_hash_find'
    1  too many arguments to function 'zend_hash_get_current_data_ex'
    2  too many arguments to function 'zend_hash_get_current_key_ex'
    11  too many arguments to function 'zend_hash_index_find'
    3  unknown type name 'zend_uint'
    1  used struct type value where scalar is required
    1  'zend_hash_get_current_data' undeclared (first use in this function)
    1  'zend_hash_index_update' undeclared (first use in this function)
    1  'zend_hash_merge' undeclared (first use in this function)
    5  'zend_hash_update' undeclared (first use in this function)
    2  'zval' has no member named 'type'
    4  'ZVAL_STRING' undeclared (first use in this function)

As you can see most of this stuff is related to Zend Hash API, which will be a
big task.

9. RETURN_STRING AND ZVAL_STRING Shims

To return strings from the extension as ZVAL these two macros are regularly
used. They need to be shimmed as well.

.. code-block:: c

    #if PHP_MAJOR_VERSION < 7
    #define _ZVAL_STRING(str, len) ZVAL_STRING(str, len, 0)
    #define _RETURN_STRING(str) RETURN_STRING(str, 0)
    #else
    #define _ZVAL_STRING(str, len) ZVAL_STRING(str, len)
    #define _RETURN_STRING(str) RETURN_STRING(str)
    #endif

10. Remove usage of zend_uint

In PHP5 a ``zend_uint`` was defined as ``unsigned long`` and is mostly replaced
with a new type ``uint32_t`` in PHP7 code. The only place I use this for is
accessing the garbage collection statistics, which are saved in ``uint32_t``
now.

11. First Hash API changes

The Upgrading docs are `very detailed about the Hash API changes
<https://wiki.php.net/phpng-upgrading#hashtable_api>`_. Most notably
keys are now represented as ``zend_string`` and the find methods return
the values instead of writing them to a void pointer-pointer.

These changes are so drastic that it is not really possible to write good shims
for these API. My first easy change looks this now:

.. code-block:: c

    #if PHP_MAJOR_VERSION < 7
        if (zend_hash_find(ht, key, len, (void**)&value) == SUCCESS) {
            result = *value;
        }
    #else
        zend_string *key_str = zend_string_init(key, len, 0);
        result = zend_hash_find(ht, key_str);
        zend_string_release(key_str);
    #endif

But I need to try anyways so lets introduce some static inline functions
for compatibility between the different hash apis. The PHP7 API is much nicer,
so lets translate PHP5 to PHP7, for example for ``zend_hash_index_find``:

.. code-block:: c

    static zend_always_inline zval* zend_compat_hash_index_find(HashTable *ht, zend_ulong idx)
    {
    #if PHP_MAJOR_VERSION < 7
        zval **tmp, *result;

        if (zend_hash_index_find(ht, idx, (void **) &tmp) == FAILURE) {
            return;
        }

        result = *tmp;
        return result;
    #else
        return zend_hash_index_find(ht, idx);
    #endif
    }

The new hash API only safes zvals and not void pointers anymore. But luckily
there are some functions that still allow you working with pointers, for
``zend_hash_update`` I introduced the following compat function:

.. code-block:: c

    static zend_always_inline void zend_compat_hash_update_ptr_const(HashTable *ht, const char *key, strsize_t len, void *ptr, size_t ptr_size)
    {
    #if PHP_MAJOR_VERSION < 7
        zend_hash_update(ht, key, len+1, ptr, ptr_size, NULL);
    #else
        zend_hash_str_update_ptr(ht, key, len, ptr);
    #endif
    }

12. zend_string - They are Everywhere!

.. image:: /_static/zend_string.jpg

The Tideways extension codebase uses strings a lot that are also saved as keys
of arrays. With PHP7 this would somehow need to be converted to use
``zend_string``.  Luckily there is also a set of new hash API functions that
still allow you to work with char and length.  It does create a temporary
``zend_string`` for each call, but that is fine for the first migration.

Following all errors related to the zend hash API I created lots of inline
functions that #if/else over the PHP version.

In the end I have a good number of ``zend_compat_hash_*`` functions that work
one way or the other on PHP5 and PHP7. This works very well for arrays that
handle zvals, however not so good for ones that safe longs or callbacks, but
this could very well be my own stupidity.  I worked around with inline macros
here to fix this.

I got it to compile after some hours of fixing all the hash API things.

13. ``*zval`` and ``MAKE_STD_ZVAL`` are gone

The first problem after running the tests for the first time: ``MAKE_STD_ZVAL``
macros is gone and it is used in a great number of functions that according
to upgrading should now use ``zval`` instead of ``zval*`` and no malloc
anymore.

I got a hint in the php-mustache PHP7 Pull-Request how to work around this:

    #if PHP_MAJOR_VERSION < 7
    #define _DECLARE_ZVAL(name) zval * name
    #define _ALLOC_INIT_ZVAL(name) ALLOC_INIT_ZVAL(name)
    #define hp_ptr_dtor(val) zval_ptr_dtor(&val);
    #else
    #define _DECLARE_ZVAL(name) zval name ## _v; zval * name = &name ## _v
    #define _ALLOC_INIT_ZVAL(name) ZVAL_NULL(name)
    #define hp_ptr_dtor(val) zval_ptr_dtor(val);
    #endif

I added the  ``hp_ptr_dtor`` macro myself to fix deallocation accross versions.

14. Changes to ``zend_execute_ex`` and ``zend_execute_internal``

These function pointers are used to hook into function calls for both userland
and internal functions, which we use for profiling. Starting with PHP7 it seems
that you have to overwrite them in module init (MINIT), because later it will
not be recognized anymore. Joe Watkins helped me solve this issue and he
mentioned that this is due to different Opcodes being generated.

So I had to move function pointer overwrites to MINIT and check for the
Profiler being enabled or not, to decide how to continue.

The first commit for this is `ed274c00365705287c6b170a30cf6d43961ccb25
<https://github.com/tideways/php-profiler-extension/commit/ed274c00365705287c6b170a30cf6d43961ccb25>`_,
with refactorings and bugfixes in the next 4 commits.

15. How to zval?

Quite a number of functions now need to be modified to account for PHP7 zval
handling. This looks like a deal-breaker to get it working on both cases,
because there is just too much code that accesses the global zvals.

I started with a new branch that only targets php7 for now, to get a feel for
the necessary changes. This went quite well

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
