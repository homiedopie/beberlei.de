
Exim4 and Virtual Users .forward Files
======================================

Some days ago I began to wonder why some mails in mail account were
filtered by Exims .forward file why some are not. It took until today
that I found out what was the problem and how to fix it.

I implemented a virtual users/domains system for Exim using several
different documentations and tutorials. Right now some parts of my
system include the documentation on

`http://www.tty1.net/virtual\_domains\_en.html <http://www.tty1.net/virtual_domains_en.html>`_

Now the problem is that the userforward router is only working for
accounts whose $local\_part is an existing system user. I came up with
the following additional router that solves the problem. Its written for
the MySQL table layout that is specified in the Tutorial above.

    ::

        virtualuserforward:
          debug_print = "R: virtualuserforward for $local_part@$domain"
          driver = redirect
          domains = +local_domains
          file = ${lookup mysql{SELECT CONCAT(home,'.forward') AS forward FROM users \
                WHERE id='${quote_mysql:$local_part}@${quote_mysql:$domain}'}}
          no_verify
          no_expn
          check_ancestor
          directory_transport = address_directory
          file_transport = address_file
          pipe_transport = address_pipe
          reply_transport = address_reply
          allow_filter

          user = ${lookup mysql{SELECT uid FROM users \
                WHERE id='${quote_mysql:$local_part}@${quote_mysql:$domain}'}}
          group = ${lookup mysql{SELECT gid FROM users \
                WHERE id = '${quote_mysql:$local_part}@${quote_mysql:$domain}'}}

Now each virtual user is using the .forward file in its actual system
user account home directory. The next problem was: $home is not defined
in this case in the .forward file syntax: Its empty. So replacing $home
with its obvious path leads to the final solution.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>