:author: beberlei <kontakt@beberlei.de>
:date: 2008-02-12

PDT: Back to easyeclipse with PHP extension
===========================================

I am disappointed by `PDT <http://www.eclipse.org/pdt/>`_ for Eclipse.
The current version strikes my rather old machine with "just" 512mb to
death. Building projects is not possible even when assigning eclipse all
my available memory, because of an Java Heap Error (`See this blog
post <http://blog.wolff-hamburg.de/archives/20-Migrating-to-PDT.html>`_).
This effectivly hinders you to use all the completion and hint features,
because PDT does not know about any functions, classes and their phpdoc
descriptions.

PDT is also missing some very important features. Marking all occurances
of a function, class, constant or variable on click for example. PHP
Errors and Warnings are display in a way so that you won't find them and
if you do, you won't understand what they mean.

So I am going back to my easyeclipse with php combination, which always
worked well, the only problem being that it is no longer under active
development. At least it has all the features I need for now.
