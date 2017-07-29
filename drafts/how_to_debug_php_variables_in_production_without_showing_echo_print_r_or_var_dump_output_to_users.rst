How to debug PHP variables in production without echo, print_r or var_dump output to users
==========================================================================================

We are used to PHP's powerful and simple toolset of `echo`, `print_r` and
`var_dump` functions that allow inspecting the current state of variables by
printing them diretly to the current page. On a development machine this
doesn't cause harm and is an extremely quick and simple way to identify and
squash bugs.

But what if you have a bug in production that you cannot reproduce on your
development server and need to debug the problem directly in production?

Let's be honest, debugging in production with `echo`, `print_r` and `var_dump`
is the easiest technique to fall back to because we are used to this strategy
of building PHP scripts.

But how to safely debug in production without printing variables so that our
users can see them? Program variables could potentially contain sensitive
information like password, api tokens or other secrets that we don't want to
show users.

This is an embarrising question to ask as a beginner, because you are in for
some harsh feedback. More advanced development practices such as unit-testing,
xdebug and central logging make this debugging approach unneeded or simply not
feasible. But still you get recommendations of upgrading your professional
debugging game with techniques that require hours, days or month to setup and
master.

**Your bug needs to be squashed now.**. Not every project has the requirement,
budget or technical stack to make this possible with the advanced tooling and
techniques that exist.

And there are other problems with the usual "helpful" suggestions:

You don't have enough information to write a re-produce case, because the
inputs causing the failure are not known to you.

You cannot easily enable xdebug for the duration of your debugging session.

You don't have central logging setup where you can easily send messages from
your program.

This was all the case for one of my students when she debugged a program she
was working on and she asked me for help. While teaching the advanced
techniques is surely important, I want to show you a basic technique that is
in my toolbox forever and usually safes the day without first spending time
setting up tools.

The functions `error_log` and `syslog` can directly send messages to a log-file
on your server with zero configuration necessary. But they can only handle
string messages, so one piece missing to serialize arrays or objects that
you want to inspect is `json_encode`, not the perfect solution but helpful when
inspecting complex data-structures 80% of the time.

.. code-block:: php

    error_log(json_encode($data));

The error_log file is either the Nginx or Apache error.log or a file configured
in the INI setting `error_log` that you can find by calling `echo
ini_get("error_log");`.

    syslog(LOG_INFO, json_encode($data));

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
