|build| |coverage| |python| |license| |docs| |status|

########
vmupdate
########

**vmupdate** is a command line utility used to keep your virtual machines up to date. It searches your computer for
virtualizers, queries them for a list of VM's, and runs the appropriate update commands.

.. contents::
    :local:
    :depth: 1
    :backlinks: none

`Read the docs <http://vmupdate.readthedocs.org>`_ for more details.

************
Installation
************

The recommended installation tool is **pip**:

.. code-block:: bash

    $ pip install vmupdate

***************
Getting Started
***************

Create a *vmupdate.yml* file with the credentials to login to your virtual machines:

.. code-block:: yaml

    Credentials:
      Username: myuser
      Password: mypass


And pass that file to the utility:

.. code-block:: bash

    $ vmupdate --config "/path/to/config/vmupdate.yaml"

**Note:** This method is included for simplicity, but is not recommended due to the inherent insecurity of a plaintext
password. Read the `Configuration <http://vmupdate.readthedocs.org/en/stable/configuration.html>`_ documentation for
more options.

********
Features
********

This list will continue expanding with later iterations of the utility.

============
Virtualizers
============

* Windows
    * VirtualBox

======
Guests
======

* Arch
    * pacman
* Ubuntu
    * apt-get


.. |build| image:: https://img.shields.io/travis/CorwinTanner/vmupdate.svg
    :target: https://travis-ci.org/CorwinTanner/vmupdate

.. |coverage| image:: https://img.shields.io/coveralls/CorwinTanner/vmupdate.svg
    :target: https://coveralls.io/github/CorwinTanner/vmupdate

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/CorwinTanner/vmupdate/blob/master/LICENSE

.. |docs| image:: https://img.shields.io/badge/docs-latest-blue.svg
    :target: http://vmupdate.readthedocs.org

.. |python| image:: https://img.shields.io/pypi/pyversions/vmupdate.svg
    :target: https://github.com/CorwinTanner/vmupdate

.. |status| image:: https://img.shields.io/pypi/status/vmupdate.svg
    :target: https://github.com/CorwinTanner/vmupdate
