
Import and PYTHONPATH Problems with PyDev and Linux
===================================================

Today is began to configure my `PyDev <http://pydev.sf.net>`_ Eclipse
enviroment since I want to learn Python and need it for a programming
aspect of my forthcoming diploma thesis. I ran into several difficulties
getting the plugins run dialog to work. It seems that configuring the
python interpreter under linux and adding all the correct include paths
is not enough, even when following the `PyDev
FAQ <http://pydev.sourceforge.net/faq.html#how_do_i_configure_my_pythonpath>`_.

Nearly giving up I came up with sort of a hack to get it running.
Eclipse can execute arbitrary "External Tools" (Find it at: "**Run ->
External Tools -> Open External Tools Dioalog**"). I used this facility
to integrate an external tool "Python" with path "**/usr/bin/python**".
Now to automatically execute the currently active python script, you can
specify the line: "**${resource\_loc}**" in the arguments field of the
dialog and you're good to go.

You now circumvented the PyDev internal execution scheme and work with
the pure command line interpreter. This way all the problems of PyDev
with the PythonPath, Symlinks and whatever are gone.

**Update:** Another note maybe, you can also add the action "running the
last used external tool again" as keyboard shortcut in the Eclipse
preferences. This simplifies the execution even more.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>