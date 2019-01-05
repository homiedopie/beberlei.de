Integrate Ansible Vault with 1Password Commandline
==================================================

We are using Ansible to provision and deploy Tideways in development and
production and the Ansible Vault feature to unlock secrets on production.
Since we recently introduced 1Password I integrated them both and unlock the
Ansible Vault using 1Password.

This way we can centrally change the Ansible Vault password regularly, without
any of the developers with access to production/deployment needing to know the
actual password.

To make this integration work, you can setup 1Password CLI to query your
1Password vault for secrets after logging in with password and two factor
token. 

Then you only need a bash script to act as an executable `Ansible Vault
password file <https://docs.ansible.com/ansible/latest/user_guide/vault.html#providing-vault-passwords>`_.

First, `download and install
<https://support.1password.com/command-line-getting-started/>`_ the 1Password
CLI according to their documentation.

Next, you need to login with your 1Password account explicitly passing email,
domain and secret key, so that the CLI can store this information in a
configuration file.

::

    $ op signin example.1password.com me@example.com
    Enter the Secret Key for me@example.com at example.1password.com: A3-**********************************
    Enter the password for me@example.com at example.1password.com: 
    Enter your six-digit authentication code: ******

After this one-time step, you can login more easily by just specifiying ``op
signin example``, so I create an alias for this in ``~.bash_aliases`` (I am on
Ubuntu).

::

    alias op-signin='eval $(op signin example)'
    alias op-logout='op signout && unset OP_SESSION_example'

The eval line makes sure that an environment variable ``OP_SESSION_example`` is
set for this terminal/shell only with temporary access to your 1Password vault
in subsequent calls to the ``op`` command. You can use ``op-logout`` alias to
invalidate this session and logout.

Then I create the bash script in ``/usr/local/bin/op-vault`` that is used as
Ansible Vault Password File. It needs to fetches the secret and print it to the
screen.

::

    #!/bin/bash
    VAULT_ID="1234"
    VAULT_ANSIBLE_NAME="Ansible Vault"
    op get item --vault=$VAULT_ID "$VAULT_ANSIBLE_NAME" |jq '.details.fields[] | select(.designation=="password").value' | tr -d '"'

This one liner uses the command ``jq`` to slice the JSON output to print only
the password. The ``tr`` command trims the double quotes around the password.

Make sure to configure the ``VAULT_ID`` and ``VAULT_ANSIBLE_NAME`` variables to
point to the ID of your vault where the secret is stored in, and its name in
the list. To get the UUIDs of all the vaults type ``op list vaults`` in your
CLI.

Afterwards you can unlock your Ansible Vault with 1Password by calling:

::

    ansible-playbook --vault-password-file=/usr/local/bin/op-vault -i inventory your_playbook.yml

This now only works in the current terminal/shell, when you called ``op-signin`` before to enter password and 2 factor token.

.. author:: default
.. categories:: none
.. tags:: Deployment, DevOps, Ansible, Automation
.. comments::
