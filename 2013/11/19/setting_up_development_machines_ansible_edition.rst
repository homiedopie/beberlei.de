Setting up development machines: Ansible edition
================================================

A little over a year ago I posted on using `Puppet for setting up development
machines
<http://www.whitewashing.de/2012/06/03/setting_up_development_machines_with_puppet.html>`_.
This approach prooved useful as during that time I did setup a new machine
several times and benefited from the mostly automatic installation with Puppet.
Github is thinking the same on a bigger scale. Earlier this year they
introduced `Boxen <https://github.com/blog/1345-introducing-boxen>`_ which is
using Puppet to setup mac-development machines.

The space of deployment- and configuration management tools
is exploding these last years and it is not always feasible to evaluate all of
them. The benefit of Puppet over all these tools is its huge userbase and
online resources. However the steep learning curve can be a huge pain coupled
with the fact that most of the modules online are not reusable at all and
mostly serve a documentation for "how not to work with Puppet". On top of that
Puppet is only for configuration management and not suitable for deployment
of applications.

Introduction to Ansible
-----------------------

I came across a `blog post on Ansible
<http://labs.qandidate.com/blog/2013/11/15/first-steps-with-ansible/>`_ by the
awesome guys at Qandidate.com which lead me to investigate `Ansible
<http://ansibleworks.com>`_. It is essentially a hybrid between Capistrano and Puppet,
solving both the deployment and configuration management problems with a focus
on simplicity. In fact the learning curve of Ansible is much more flat than
that of Puppet and you can read the whole documentation and understand even the
advanced concepts in a few hours.

Ansible is used from a developer- or continuous-integration-machine, which
executes tasks on hosts from an inventory. You only need SSH servers running
and private keys to connect to them to get it working. With the inventory of
hosts to operate on, you can chose to execute ad-oc commands using the
`ansible` command or playbooks using the `ansible-playbook` command. Playbooks
are files written in YAML.

`Read Sanders post on the Qandidate blog
<http://labs.qandidate.com/blog/2013/11/15/first-steps-with-ansible>`_ to get an introduction to Ansible.

Development-Machine Setup
-------------------------

Using Ansible to setup a development machine is a bit pointless, given that
Ansible excels at remote task execution and distribution. The benefit in
development-machine setup over Puppet is the simplicity of configuration
compared to Puppet modules + DSL.

For demonstration I have converted the puppet examples from my blog post on
Puppet to Ansible.  To start we have to create a folder and create a new file
`inventory` in it containing our local machine:

    localhost   ansible_connection=local

This is necessary to convince the remote task execution part of Ansible that
localhost exists and there is no SSH necessary to get into that machine.

Now I can create playbooks for the different tools I might want to install and
setup, such as Vim in a `vim.yml`:

    ---
    - hosts: localhost
      tasks:
        - name: Install VIM
          apt: pkg=vim state=present
          sudo: yes
        - name: Install Dotfiles
          git: >
            repo=git@github.com/beberlei/vim-dotfiles.git
            dest=/home/${ansible_user_id}/.vim
        - name: Create .vimrc Symlink
          file: >
            src=/home/${ansible_user_id}/.vim/vimrc
            dest=/home/${ansible_user_id}/.vimrc
            state=symlink
        - name: Compile and Install Command-T plugin
          command: >
            rake make
            chdir=/home/${ansible_user_id}/.vim/bundle/Command-T
            creates=/home/${ansible_uesr_id}/.vim/bundle/Command-T/command-t.recipe

You can see here, tasks are a list of commands to execute. They are always
executed in order and stop when the first task in the chain fails. Like in
puppet you try to make those tasks idempotent through flags such as `creates`,
signaling when a task needs to be or was already executed. I can optionally
use sudo to run commands such as installing packages.

To execute the playbook I call:

    $> ansible-playbook -K -i inventory vim.yml

With the ``-i`` flag I define the pool of hosts to run on, in our case the
local machine and the playbook applies the `hosts` filter to that inventory.
The `-K` parameter prompts me to enter the sudo password for my Ubuntu machine,
otherwise the tasks will fail.

Conclusion
----------

Compared to Puppet, the configuration management of Ansible simplifies a lot of
the assumptions for example on ordering and reusability of tasks. For a
part-time "devop" like me this is great news, as I don't need to understand a
complex tool and can focus on solving problems.

On top of that the deployment features of Ansible with parallel remote
execution over SSH make Ansible a powerful tool that I hope to use much more in
the future.

.. author:: default
.. categories:: Devops
.. tags:: Ansible
.. comments::
