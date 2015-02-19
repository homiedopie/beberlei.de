Vagrant, NFS and NPM
====================

I have ranted about Node.JS and NPM on Twitter before, costing me lots of time,
so I have to make up for this now and offer some solutions.

One problem I regularly have is the following: I have a Vagrant/Virtualbox
using NFS and want to run NPM inside of that. Running it inside the box
is necessary, because I don't want everyone using the box have to setup the
node stack.

However running ``npm install`` on an NFS share doesn't work as per `issue
#3565 <https://github.com/npm/npm/issues/3565>`_ because a chmod fails and
apparently from the ticket, this is not going to be fixed.

I finally got it working with a workaround script by `Kevin
Stone <https://github.com/kevinastone>`_ that mimics NPM, but
moves the ``package.json`` to a temporary directory and then rsyncs its back:

::

    #!/bin/bash
    # roles/nodejs/files/tmpnpm.sh

    BASE_DIR=${TMPDIR:-/var/tmp}
    ORIG_DIR=$PWD
    HASH_CMD="md5sum"

    DIR_NAME=`echo $PWD | $HASH_CMD | cut -f1 -d " "`

    TMP_DIR=$BASE_DIR/$DIR_NAME
    mkdir -p $TMP_DIR

    pushd $TMP_DIR

    ln -sf $ORIG_DIR/package.json
    npm $1

    # Can't use archive mode cause of the permissions
    rsync --recursive --links --times node_modules $ORIG_DIR

    popd

Integrating this into my Ansible setup of the machine it looked like this:

::

    # roles/nodejs/tasks/main.yml
    # More tasks here before this...
    - name: "Install npm workaround"
      copy: >
          src=tmpnpm.sh
          dest=/usr/local/bin/tmpnpm
          mode="0755"

    - name: "Install Global Dependencies"
      command: >
          /usr/local/bin/tmpnpm install -g {{ item }}
      with_items: global_packages

    - name: "Install Package Dependencies"
      command: >
          /usr/local/bin/tmpnpm install
          chdir={{ item }}
      with_items: package_dirs

Where ``global_packages`` and ``package_dirs`` are specified from the
outside when invoking the role:

::

    # deploy.yml
    ---
    - hosts: all
      roles:
        - name: nodejs
          global_packages:
            - grunt-cli
          package_dirs:
            - "/var/www/project"

This way the Ansible Node.JS role is reusable in different projects.

.. author:: default
.. categories:: NodeJS
.. tags:: NPM, Ansible
.. comments::
