`|Build Status| <https://travis-ci.org/nocarryr/AWS-Identity-Manager>`_
`|Coverage
Status| <https://coveralls.io/github/nocarryr/AWS-Identity-Manager?branch=master>`_

AWS-Identity-Manager
====================

Command line tool to store credentials for multiple AWS accounts and
quickly switch between them.

Installation
------------

To install using pip: ``pip install aws-identity-manager`` Or download
the `latest
release <https://github.com/nocarryr/AWS-Identity-Manager/releases/latest>`_
and install by running: ``python setup.py install``

Usage
-----

Start the interactive command line tool: ``awsidentity``

Then use the following commands:

-  ``save`` Save credentials (if any) found in your existing config
   files for later use
-  ``add`` Allows you to add a new set of credentials (identity)
-  ``edit`` Make changes to existing identity
-  ``change`` Select one of your stored identies and modifies (or
   creates) the configuration files for most AWS client libraries
-  ``import`` Import identities from a csv file downloaded from the IAM
   Console (created whenever you add new users)

Additional Info
~~~~~~~~~~~~~~~

All of the credentials are saved by default in your home directory:
``.aws-identity-manager/identities.json`` The scripts are designed to
keep the permissions of this as well as the modified config files
secured and only accessible to the current user. Before any changes are
made to any existing AWS config files, they are backed up:
``~/.aws/credentials.bak`` This is only done if the backup filename
doesn't already exist though. In other words, it would be a good idea to
have your credentials somewhere safe before running the script.

.. |Build
Status| image:: https://travis-ci.org/nocarryr/AWS-Identity-Manager.svg?branch=master
.. |Coverage
Status| image:: https://coveralls.io/repos/github/nocarryr/AWS-Identity-Manager/badge.svg?branch=master


