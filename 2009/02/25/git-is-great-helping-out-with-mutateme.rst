
Git is great: Helping out with MutateMe
=======================================

These last days I had fun with `Padraic Bradys
MutateMe <https://github.com/padraic/mutateme/tree>`_ project. It
dynamically changes your code (using PECL Runkit extension) and checks
weather your test cases fetch the errors occurring from changing the
source code. This is a great addition to having a test suite, because it
finds all the problematic test cases, that try to do too much and fail
to cover the code correctly.

I have also contributed to the MutateMe project already and this was
only possible due to Git and `GitHub <http://www.github.com>`_, which
makes contributing to any project easy like writing a hello world
example in a random programing language. As such I have to agree with
Padraic: `I love Git,
too! <http://blog.astrumfutura.com/archives/390-Mutation-Testing-MutateMe-0.2.0alpha-Released.html>`_
He already integrated my and `Sebastians <http://www.phpunit.de>`_
changes back into the master and we didn't have to focus on merging,
communication and integration alot.

My `PUMA project <http://github.com/beberlei/puma/tree/master>`_ is also
hosted on GitHub (although nobody has looked into that yet), but I am
beginning to write a complete Runner now that calls all three components
`PHPUnit <http://www.phpunit.de>`_, `PDepend <http://www.pdepend.org>`_
and CodeSniffer at once and directly processes the results. When this is
done, I will pack it all up as a PEAR package for anyone to test out.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>