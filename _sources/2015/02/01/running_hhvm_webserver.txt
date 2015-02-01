Running HHVM with a Webserver
=============================

I haven't used `HHVM <http://hhvm.com>`_ yet because the use-case for the
alternative PHP runtime didn't came up. Today I was wondering if our `Qafoo
Profiler <https://qafoolabs.com>`_ would run out of the box with HHVM using the
`builtin XHProf extension <http://docs.hhvm.com/manual/en/ref.xhprof.php>`_
(Answer: It does).

For this experiment I wanted to run the wordpress blog of my wife on HHVM
locally. It turns out this is not very easy with an existing LAMP stack,
because mod-php5 and mod-fastcgi obviously compete for the execution of `.php`
files.

Quick googling didn't turn up a solution (there probably is one, hints in the
comments are appreciated) and I didn't want to install a Vagrant Box just for
this. So I decided to turn this into a sunday side project. Requirements: A
simple webserver that acts as proxy in front of HHVMs Fast-CGI. Think of it as
the "builtin webserver" that HHVM is missing.

This turns out to be really simple with Go, a language I use a lot for small
projects in the last months.

The code is `very simple plumbing <https://github.com/beberlei/hhvm-serve/blob/master/hhvm-serve.go>`_
starting with a HTTP Server that accepts client requests, translates them to FastCGI
requests, sending them to HHVM and then parsing the FastCGI Response to turn it into a
HTTP Response.

As a PHP developer I am amazed how Go makes it easy to write this kind of
infrastructure tooling. I prefer PHP for everything web related, but as I tried
to explain in `my talk at PHPBenelux last week
<https://joind.in/event/view/2564>`_, Go is a fantastic language to write
small, self-contained infrastructure components (or Microservices if you want a
buzzword).

Back to playing with HHVM, if you want to give your application a try with HHVM
instead of ZendEngine PHP it boils down to `installing a prebuilt HHVM package
<https://github.com/facebook/hhvm/wiki/Prebuilt-Packages-for-HHVM>`_ and then
using my ``hhvm-serve`` command:

    $ go get github.com/beberlei/hhvm-serve
    $ hhvm-serve --document-root /var/www
    Listening on http://localhost:8080
    Document root is /var/www
    Press Ctrl-C to quit.

The server passes all the necessary environment variables to HHVM so that
catch-all front-controller scripts such as Wordpress ``index.php`` or Symfony's
``app.php`` should just work.

If you don't have a running Go Compiler setup this few lines should help you out on
Ubuntu:

    $ sudo apt-get install golang
    $ GOPATH=~/go
    $ mkdir -p ~/go/{src,bin,pkg}
    $ PATH="$GOPATH/bin:$PATH"

You should put the ``$GOPATH`` and ``$PATH`` changes into your bashrc to make this
a permanent solution.

Starting to run HHVM, a Wordpress installation is a good first candidate to
check on, as I knew from HHVM team blog posts that Wordpress works. Using a
simple siege based benchmark I was able to trigger the JIT compiler and the
Profiler charts showed a nice performance boost minute after minute as HHVM
replaces dynamic PHP with optimized (assembler?) code.

.. author:: default
.. categories:: Go
.. tags:: none
.. comments::
