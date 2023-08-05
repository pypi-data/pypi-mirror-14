.. image:: https://travis-ci.org/CorwinTanner/vmupdate.svg?branch=master
    :target: https://travis-ci.org/CorwinTanner/vmupdate

********
vmupdate
********

**vmupdate** is a command line utility used to keep your virtual machines up to date. It searches your computer for
virtualizers, queries them for a list of VM's, and runs the appropriate update commands.

.. contents::
    :local:
    :depth: 1
    :backlinks: none

============
Installation
============

The recommended installation tool is **pip**:

.. code-block:: bash

    $ pip install vmupdate

=====
Usage
=====

Running vmupdate is just as easy:

.. code-block:: bash

    $ vmupdate

Or specify a custom config:

.. code-block:: bash

    $ vmupdate --config "/path/to/config.yaml"

=============
Configuration
=============

-----
Basic
-----

This method is included for simplicity, but is not recommended due to the inherent insecurity of a plaintext password.

.. code-block:: yaml

    Credentials:
      Username: myuser
      Password: mypass

--------
Keyring
--------

If a ``Password`` is not specified and ``Use Keyring`` is ``True`` (default) the password will be retrieved from your host
OS's keyring provider under the name ``vmupdate``.

.. code-block:: yaml

    Credentials:
      Username: myuser

--------
Machines
--------

The ``Machines`` section of the config file allows some options to be overriden at the VM level by name.

.. code-block:: yaml

    Machines:
      My Ubuntu Box:
        Username: myuser1
        Password: mypass
      My Arch Box:
        Username: myuser2
        Use Keyring: true

If a ``Password`` is not specified and ``Use Keyring`` is ``True`` the password will be retrieved from your host OS's
keyring provider under the name of the VM (i.e. ``My Arch Box``).

========
Features
========

This list will continue expanding with later iterations of the tool.

------------
Virtualizers
------------

* Windows
    * VirtualBox

------
Guests
------

* Arch
    * pacman
* Ubuntu
    * apt-get

===============
Troubleshooting
===============

----
SSH
----

SSH is used to communicate with VM's so you will need an SSH server enabled on each virtual machine. This is
often then case by default with many \*nix installations, but may have to be installed separately.

---------------
Port Forwarding
---------------

An attempt will be made to forward port 22 on each VM to a unique port on the host if such a forward does not already
exist. This only needs to be done once per virtual machine and can only occur if the VM is in a *stopped* state. If
the automatic port forwarding fails, you can configure it yourself using your virtualizer.
