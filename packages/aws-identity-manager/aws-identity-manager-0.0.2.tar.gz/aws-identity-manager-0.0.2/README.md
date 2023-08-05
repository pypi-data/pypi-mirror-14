[![Build Status](https://travis-ci.org/nocarryr/AWS-Identity-Manager.svg?branch=master)](https://travis-ci.org/nocarryr/AWS-Identity-Manager) [![Coverage Status](https://coveralls.io/repos/github/nocarryr/AWS-Identity-Manager/badge.svg?branch=master)](https://coveralls.io/github/nocarryr/AWS-Identity-Manager?branch=master)

# AWS-Identity-Manager
Command line tool to store credentials for multiple AWS accounts and quickly switch between them.

## Installation
To install using pip:
```
pip install aws-identity-manager
```
Or download the [latest release](https://github.com/nocarryr/AWS-Identity-Manager/releases/latest) and install by running:
```
python setup.py install
```

## Usage
Start the interactive command line tool:
```
awsidentity
```

Then use the following commands:

* `save` Save credentials (if any) found in your existing config files for later use
* `add` Allows you to add a new set of credentials (identity)
* `edit` Make changes to existing identity
* `change` Select one of your stored identies and modifies (or creates) the configuration files for most AWS client libraries
