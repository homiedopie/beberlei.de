In defense of functions in PHP: SOLID principles
================================================

::

    tl;dr: You can achieve SOLID with functions and don't necessarily need
    to migrate to the OOP paradigm to get dependency inversion, decoupling
    and testability.

This blog post will argue that it is not necessary to use OOP to achieve high
code-reuse, decoupling and testability. Existing projects with functions should
instead move towards more functional code, which is much easier to refactor to
and doesn't alienate the community of users that are used to the current style.

Nowadays developing in PHP is mostly using classes/objects and this trend will
increase with Drupal8 now moving towards OOP as well. The only major PHP
software projects I know that are still based largely on functions are
Wordpress and phpBB (maybe Mediawiki?).

Why are objects favored over functions? In general, because we learned that
they allow better code-reuse, decoupling, testability, runtime binding of
dependencies and avoid global state. The fundamental principles behind these
claims are the `SOLID principles
<http://en.wikipedia.org/wiki/SOLID_(object-oriented_design)>`_.

Systems based on functions try to emulate some properties of OOP with two
different kinds of hooks, often relying on magic and global state, which
results in untestable and code that is difficult to understand.

But you can follow the SOLID principles as easily with functions and get rid of
global state without resorting to magic. To achieve this you should move from
the imperative/procedural paradigm towards more functional instead of the
object-oriented paradigm.

What are the differences between those paradigms? In object-oriented paradigm
we have mutable state and we couple data+behavior. In the functional paradigm
we seperate data and behavior and focus on immutable state. Immutable state
means no modifications are possible after creation, instead only new values are
created. See `Anthony's video
<http://blog.ircmaxell.com/2012/11/programming-with-anthony-paradigm-soup.html>`_
for more details on different programming paradigms.

Example
-------

Let's dive into code to explain how to achieve SOLID with functions. Take the
following piece of code from a really simple wordpress plugin. It retrieves
an option from the database to print a header, but only when we are on the
blog with id `4`.

.. code-block:: php

    <?php
    // my plugin, register my function with Wordpress hooks
    add_action('send_headers', 'add_header_xua');

    function add_header_xua()
    {
        if ($GLOBALS['blog_id'] === 4) {
            header(sprintf('X-UA-Compatible: %s', get_option('myplugin_xuacompatible'));
        }
    }

The Wordpress core function that invokes the hook and triggers my function
looks roughly like this:

.. code-block:: php

    <?php
    class WP
    {
        public function send_headers()
        {
            // lots of stuff happening here...
            do_action_ref_array('send_headers', array(&$this));
        }
    }

The function ``do_action_ref_array`` checks all themes and plugins for
functions that registered using ``add_action($hookName, $functionName);``. The hook is an
observer as it cannot influence the ``WP#send_headers()`` call.

We can observe multiple things here that are annoying about our ``add_header_xua``
function:

1. It uses ``$GLOBALS`` to access the current blog id.
2. It calls another function ``get_option`` directly, without a chance to replace
   that call at runtime.
3. The function ``add_action`` clearly registers the callback somewhere global,
   because it is accessible from ``do_action_ref_array`` inside Wordpress.

Assume for this blog post, that we can change how Wordpress works internally, then
one approach forrefactoring towards SOLID princples and away from global state
might follow the steps described below.

Step 1: Remove global state
---------------------------

Global state is context information to the function that is currently executed.
Because it is globally defined that state entails drawbacks such as difficult
to understand side-effects and are hard to test.

Lets make that global state explicit by introducing a context for our function
call.

.. code-block:: php

    <?php
    class WordpressContext
    {
        public $blogId;
        // much more context details here
    }

We could introduce an array as context ``$wordpressContext = array('blog_id' =>
4);`` to avoid using a class, but passing around huge arrays of data hurts
readability of code very much. Introducing an object here allows us to be
typesafe and help developers read the code. Take note that this does not mean
that we are now using object-oriented paradigm, since we are still seperating
data and behavior and we might design ``WordpressContext`` to be immutable in
the future.

Now assume that every hook function always gets this context passed as first
argument, with the help of some code inside ``do_action_ref_array``:

.. code-block:: php

    <?php
    function add_header_xua(WordpressContext $context)
    {
        if ($wordpressContext->blogId === 4) {
            header(sprintf('X-UA-Compatible: %s', get_option('myplugin_xuacompatible'));
        }
    }

We got rid of the global state. If we would pass the current context around
this way to all functions, we would have much more control over side-effects
and and increase testability.

Step 2: Remove hard dependency to function call
-----------------------------------------------

Our ``add_header_xua`` is not yet testable, it still calls ``get_option`` that
will directly go to the database and fetch an option value. To replace
hard coded functions, we want to use the dependency inversion principle and
inject this function instead:

.. code-block:: php

    <?php
    function add_header_xua(WordpressContext $context, callable $getOption)
    {
        if ($wordpressContext->blogId === 4) {
            header(sprintf('X-UA-Compatible: %s', $getOption('myplugin_xuacompatible'));
        }
    }

If all our hook functions recieve ``WordpressContext`` this can be handled
generically in our library. However now our hooks get arbitrary arguments, in
this case ``$getOption``, and we need to introduce a mechanism to
``add_action`` to pass additional dependencies. We decide on an array
of options that are passed as second to n-th argument to the hook function
in order:

.. code-block:: php

    <?php
    add_action('send_headers', 'add_header_xua', array('get_option'));

Step 3: Remove side-effects
---------------------------

Almost done with refactoring ``add_header_xua`` there is only the ``header``
function left, which has a side-effect on the global state. Lets remove that
side-effect here and push it into the function that is responsible for the side
effect ``WP#send_headres()``.

We pass an array of ``$headers`` into every ``send_headers`` hook and always
return the same or a modified array:

.. code-block:: php

    <?php
    function add_header_xua(WordpressContext $context, callable $getOption, array $headers = array())
    {
        if ($wordpressContext->blogId === 4) {
            $headers[] = sprintf('X-UA-Compatible: %s', $getOption('myplugin_xuacompatible'));
        }

        return $headers;
    }

We removed all side-effects now, and ``add_header_xua`` is a pure function,
with all their benefits, most notably they are easy to understand and test.

Adjusting our core by turning ``send_headers`` into a filter we get:

.. code-block:: php

    <?php
    class WP
    {
        public function send_headers()
        {
            // lots of stuff happening here...
            $headers = apply_filters('send_headers', $headers);

            foreach ($headers as $header) {
                header($header);
            }
        }
    }

Several things happened here that you cannot see without reading more of the
Wordpress code.

1. The ``header`` side-effect was encapsulated in a single location, rather
   then spread around all the hooks.

2. Passing ``$headers`` now allows us to modify headers of other filters as
   well as the headers set by the core of Wordpress itself.

3. We could make ``// lots of stuff happening here`` a filter that is
   registered by the core, which would turn the current ``WP#send_headers()``
   method into just the 4 lines of PHP above (down from 90).

Step 4: Write unit-tests
------------------------

We can now write a simple test for our function:

.. code-block:: php

    <?php
    class AddHeaderXuTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @test
         ***/
        public function it_adds_xuacompatible_header_from_option_when_blog4()
        {
            $context = new WordpressContext();
            $context->blogId = 4;

            $headers = add_header_xua($context, function () {
                return 'Foo';
            }, array());

            $this->assertEquals(array('X-UA-Compatible: Foo'), $headers);
        }
    }

Profit!

Loose Ends
----------

The solution is far from perfect, improvements are possible in multiple
areas:

- The ``add_header_xua`` function currently gets passed the whole context. If we
  grow our solution this context might contain lots of properties and objects
  and it might not be so easy to create the Context in the testing environment.
  Therefore it would be nice if we had more control over the dependencies that
  get passed to the function.

- We are just passing a ``callable $getOption`` into our function. This method
  does not enforce any contract and can make it very hard for developers to
  understand the code. However it is important to mention that this generic
  dependency is also the biggest benefit of this system, because it makes it
  extremly easy to exchange and extend code.

- ``WordpressContext`` is not immutable. Working with purely immutable
  datastructures is not possible efficiently in PHP, because the engine does
  not support this style of programming very well. This means we have to make
  pragmatic decisions about what datastructures are mutable and which are
  immutable in our PHP code. We also have to force ourselves to avoid
  mutating data and make functions pure instead.

I will discuss approaches to fix these problems in future blog posts.

Conclusion
----------

This blog post has shown that it is possible to benefit from the SOLID
principles even when not using objects to encapsulate operations. 

1. By definition a function serves a single responsibility (S). This principle
   can obviously be violated by the programmer, but in our case it is not.

2. A function also fullfils the interface segregation principle (I) perfectly,
   as it doesn't force clients to depend on additional code that they don't need.

3. Dependency Inversion (D) is achieved by passing the context and dependencies
   as arguments into the function.

Open-Closed principle (O) and Liskov-Substitution principle (L) are left out,
as they does not really apply here.

The resulting code is very simple to read and write and does not contain global
state anymore. 

This blog post doesn't show a full-fledged solution to the problem and there
are some issues that need to be tackled, however it is a good proof of concept
to show the basics of using functional approaches 

.. author:: default
.. categories:: PHP
.. tags:: PHP
.. comments::
