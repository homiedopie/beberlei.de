Virtual Machines with Vagrant, Veewee and Puppet
================================================

I have been playing with Vagrant these last days, a tool to automate Virtualbox
VM management very efficiently. Being always late to new technologies
investigating Vagrant now felt about right. I am using Virtualbox for
virtualization for about a year now but have build all my boxes manually. I
have these machines setup:

- Windows 7
- Ubuntu with lots of crazy PHP builds
- Ubuntu with Oracle, PostgreSQL for Doctrine Unit-Tests

The main benefit from this is that I don't have to clutter my main machine with
packages and dependencies that might potentially break.

To benefit from Virtualization on a larger scale I wanted to investigate
automation of box-building and was pointed to `Vagrant
<http://www.vagrantup.com>`_. This is a ruby tool that allows to copy and
modify virtualboxes on the fly. You define a basebox and inherit from this box
in your projects. Whenever you work on the project you start a copy of this
basebox and install more system-dependencies using Chef or Puppet.
That allows you to put the VM into a defined state just for this project. No
matter how many different and weird dependencies you need, they will always be
in this VM that is just created for the project and destroyed at the end of the
day.

I am using Ubuntu (currently 12.04) and tried starting with the Vagrant
example.  It fails, because their example box uses a more current Virtualbox
Guest Additions. To be able to use vagrant, you need a basebox with the
virtualbox and guest additions versions matching correctly. 

To build your own Virtualbox you can use the Vagrant plugin `Veewee
<https://github.com/jedi4ever/veewee>`_. Install it from Github to get
all the latest VM templates:

.. code-block:: bash

    $ git clone https://github.com/jedi4ever/veewee.git
    $ cd veewee
    $ sudo gem install bundler
    $ sudo bundle install
    $ alias vagrant="bundle exec vagrant"

You need Ruby and Gems installed for this to work. Veewee can be installed
using Gems, but this not necessarily gives you the version with the most recent
templates that match your own operating system version.

Now lets define our own basebox definition and copy from an existing template
that Veewee provides:

.. code-block:: bash

    $ vagrant basebox define 'beberlei-ubuntu-12.04-i386-php' 'ubuntu-server-12.04-i386'

This creates a copy from the default ubuntu server template into a folder
`definitions/beberlei-ubuntu-12.04-i386-php`. You can start modifying the files
in there to adjust the build process of the virtual machine image. For me its
important to modify the definitions.rb and add the following, otherwise
building the VMs fails:

.. code-block:: bash

    :virtualbox => { : vm_options => ["pae" => "on"]},

You can then open up the postinstall.sh and install more packages that you need
in your personal basebox. For example a LAMP stack. Do this right after the
lines that do `apt-get install -y`:

.. code-block:: bash

    export DEBIAN_FRONTEND=noninteractive
    apt-get -y install php5 php5-cli php5 mysql-server-5.5 libapache2-mod-php5

If you are done you can start building a virtualbox image with:


.. code-block:: bash

    $ vagrant basebox build

Make sure not to start typing in the console window that open ups. It is
automatically controlled from a ruby script and every change to the keysequence
breaks the building. This step takes a while. (Enough to write a blog post
while watching a boring football game for example).

When this is done, you can verify and export the VM into virtualbox/vagrant.


.. code-block:: bash

    $ veewee vbox validate 'beberlei-ubuntu-12.04-i386-php'
    $ vagrant basebox export 'beberlei-ubuntu-12.04-i386-php'
    $ vagrant box add 'beberlei-ubuntu-12.04-i386-php' 'beberlei-ubuntu-12.04-i386-php.box'

Now this box is also available as Vagrant base box. For example in a project
that we want to use with vagrant, do:


.. code-block:: bash

    $ cd myproject/
    $ vagrant init 'beberlei-ubuntu-12.04-i386-php'
    $ vagrant up
    $ vagrant ssh

Although the blog-title suggests it, Puppet hasn't been used much up to this
point. The use of puppet with Vagrant will be part of a next blog post.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
