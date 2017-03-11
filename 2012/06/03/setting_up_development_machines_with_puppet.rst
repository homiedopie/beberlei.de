Setting up Development Machines with Puppet
===========================================

I wrote `about Vagrant
</2012/05/31/virtual_machines_with_vagrant__veewee_and_puppet.html>`_ last week and
mentioned to talk about `Puppet
<http://puppetlabs.com/puppet/what-is-puppet/>`_ in the future. Before I will
dive into Puppet in combination with Vagrant I want to share my general
experiences with Puppet (beginners level, I just played with this today).

Puppet is a configuration management tool. It uses a declarative language to
describe how a system should look like. Upon invocation of puppet it attempts
to get the system from its current state into the desired state by installing
packages, executing programs/scripts and creating files/directories.

My laptop was still on Ubuntu 10.04 this morning, but for `Symfony Live
<http://live.symfony.com>`_ I needed to upgrade to 12.04. This was necessary to
run a Virtualbox VM on my laptop that I built on my 12.04 desktop. Additionally
I really like the Unity desktop and wanted to get away from the Gnome that is
in 10.04.

After a backup and fresh installation of Ubuntu I realized how many things I
have to install to get this machine productive:

- LAMP stack + a bunch of other databases and services
- Git, Svn, Hg, ..
- Virtualbox + Vagrant
- Vim with my Dot-Files, including Command-T which requires compilation,
  and a bunch of development tools such as tree, ack-grep.    
- PHP Tools (PHPUnit, PHPCS, Xdebug, Xhprof)
- Git with Author Information and global ignore file
- A bunch of .bashrc initializations
- Some open source projects I always have around (Doctrine, ...)
- Setup automatic backup with my cloud storage provider (`Strato Hidrive
  <https://www.free-hidrive.com/>`_ - they support rsync)
- and I probably forgot a bunch of tools just thinking about this today.

I realized not only virtual machines, but also their hosts (my development
machines) could be automatically setup with Puppet.

So instead of saving my ``.bash_history`` to remember the steps I automated
them using Puppet. In Puppet you define Resources of several types, for example
Files, Packages or shell commands. You group these resources together in a
``.pp`` file and then invoke ``puppet apply <file>.pp``. You can install Puppet
via ``sudo apt-get install puppet`` on Ubuntu.

The idea is to define Puppet resources in a way that they are performed once and
then the system has this resource. This means you can run puppet as often as
you want and it will only activate the missing resources.

I separate the installation process into two puppet files, one that has to be
run with root ``~/.puppet/devmachine-root.pp`` and another one that has to be run with
my own user ``~/.puppet/devmachine.pp``.

Because every dev-machine setup is unique, I will just show some
examples of my puppet file to get the message across:

::

    # /home/benny/.puppet/devmachine.pp

    # VIM Dot Files
    vcsrepo { 'vim-dotfiles': 
        path     => "/home/$id/.vim",
        ensure   => present,
        provider => git,
        source   => 'https://...'
    }

    file { 'vim-dotfiles-symlink':
        path   => "/home/$id/.vimrc",
        ensure => link,
        target => '.vim/vimrc',
        require => Vcsrepo['vim-dotfiles']
    }

    exec { 'vim-make-command-t':
        command => 'rake make',
        cwd     => "/home/$id/.vim/bundle/Command-T",
        unless  => "ls -aFlh /home/$id/.vim/bundle/Command-T|grep 'command-t.recipe'",
        require => Vcsrepo['vim-dotfiles']
    }

The three keywords ``vcsrepo``, ``file`` and ``exec`` are called types. They
define what functionality should be executed by puppet. Vcsrepo is a custom
type that you can grab `from Github
<https://github.com/puppetlabs/puppetlabs-vcsrepo.git>`_.

- The first block uses Git to make sure that in my home directory the
  ``~/.vim`` directory is a checkout of a given remote git repository.
- The second file block makes sure that ``~/.vimrc`` points to ``~/.vim/vimrc``
  using a symlink.
- The third block compiles the Command-T VIM plugin. Inside the
  exec block you can see the unless condition. This is necessary to prevent the
  command from being executed whenever ``devmachine.pp`` is executed with
  puppet. The require makes sure this resource is only activated after the dotfiles
  were installed.

Another nice example is the configuration of Git:

:: 

    # Configure Git
    exec { "git-author-name":
        command => 'git config --global user.name "Benjamin Eberlei"',
        unless => "git config --global --get user.name|grep 'Benjamin Eberlei'"
    }

    exec { "git-author-email":
        command => 'git config --global user.email "kontakt@beberlei.de"',
        unless => "git config --global --get user.email|grep 'kontakt@beberlei.de'"
    }

    exec { "git-global-ignore":
        command => "git config --global core.excludesfile /home/$id/.gitignore",
        unless  => 'git config -l --global|grep excludesfile'
    }

    file { "git-global-ignorefile":
        path => "/home/$id/.gitignore",
        ensure => present,
        content => "*.swo\n*.swp\n"
    }

Here A bunch of commands is executed unless some option is already set. At last
the global .gitingore is filled with the patterns of Vim temporary files.

I also automated all the other steps listed above, but will spare you the
details. For the LAMP Stack + PHP I used `this following Github repository
<https://github.com/dietervds/puppet-symfony2>`_ as an inspiration. It ships a
set of Puppet Modules. You can just put them into your ``~/.puppet/modules``
folder and they are then available in any of your puppet files.

I can now reuse this on the different machines: desktop at home and at work and
my laptop. Whenever I install a new tool or change some configuration of my
system I can directly put this into puppet and keep the setup synchronized on
all the machines I work with.

You can find more detailed resources on the PuppetLabs website:

- `Tutorial <http://docs.puppetlabs.com/learning/ral.html>`_
- `Type Reference <http://docs.puppetlabs.com/references/latest/type.html>`_
- `Type Cheat Sheet <docs.puppetlabs.com/puppet_core_types_cheatsheet.pdf>`_

.. author:: default
.. categories:: Automation
.. tags:: none
.. comments::
