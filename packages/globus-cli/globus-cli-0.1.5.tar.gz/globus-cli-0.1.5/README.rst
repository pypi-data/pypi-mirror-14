.. image:: https://badge.fury.io/py/globus-cli.svg
    :alt: PyPi Version
    :target: https://badge.fury.io/py/globus-cli
.. image:: https://img.shields.io/pypi/pyversions/globus-cli.svg
    :alt: Supported Pythons
    :target: https://img.shields.io/pypi/pyversions/globus-cli.svg


Globus CLI
==========

A Command Line Interface to `Globus <https://www.globus.org/>`_.

Source Code: https://github.com/globusonline/globus-cli
Documentation: http://globus.github.io/globus-cli

Installation
------------

The easiest way to install the Globus CLI is using the ``pip`` python package
manager::

    pip install globus-cli

This will automatically install the CLI and all its dependencies.

You can also get a bleeding-edge version under development directly from the
source::

    git checkout https://github.com/globusonline/globus-cli.git
    cd globus-cli
    python setup.py install

Running the CLI
---------------

Once you have the CLI installed, you should be able to use the ``globus``
command, as in :code:`globus transfer ls --endpoint-id ...`

To get started, you'll need to get tokens to authenticate to the Globus
Service. To get help info on getting tokens, just run

.. code-block:: sh

    globus login

and to see the available commands, run

.. code-block:: sh

    globus list-commands


Bugs and Feature Requests
-------------------------

Bugs reports and feature requests are open submission, and should be filed at
https://github.com/globusonline/globus-cli/issues
