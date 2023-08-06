s3import: S3 data import utility
================================

Introduction
------------

s3import is a tool for importing data from S3 to an SX Cluster. For each source
S3 bucket s3import creates a volume on the cluster and copies the keys from the
bucket to the new volume.

s3import uses boto (https://pypi.python.org/pypi/boto) and python-sxclient
(https://pypi.python.org/pypi/sxclient) and works in Python 2.7.


Installation
------------

To install s3import, run::

   $ pip install s3import

Alternatively, to install s3import from source, run::

   $ pip install <path>

or

::

   $ pip install -e <path>

replacing ``<path>`` with path to the source.


Configuration
-------------

S3
^^

Configuration for connecting with an S3 service is obtained from boto config
file. Your file should contain at least:

- ``aws_access_key_id`` in ``[Credentials]`` section, with your S3 access key
  ID as a value;
- ``aws_secret_access_key`` in ``[Credentials]`` section, with your S3 secret
  access key as a value.

Additionally, if you want to connect to an S3 service other than Amazon S3,
your file should contain:

- ``s3_host`` in ``[Credentials]`` section, with hostname of the S3 service you
  want to access;
- ``s3_port`` in ``[Credentials]`` section, with port which the S3 service
  uses.

By default, connection with S3 is secured by SSL and the SSL certificates are
verified. If you wish to change any of these behaviours, add ``is_secure =
False`` and ``https_validate_certificates = False`` respectively to the
``[Boto]`` section of your config file.

In order for boto to read the config file automatically, you should name it
``.boto`` and place it in your home directory. You can also set the environment
variable ``BOTO_CONFIG`` with the path to the configuration file you want to
use prior to running s3import.

Be wary that boto tries to read configuration options from other locations than
boto config file. For example, if a file ``~/.aws/credentials`` exists, boto
will read credential settings from there. For more information see
http://docs.pythonboto.org/en/latest/boto_config_tut.html.

Below is an example content of a configuration file::

   [Credentials]
   s3_host = s3.example.com
   s3_port = 8443
   aws_access_key_id = s3_user
   aws_secret_access_key = secret_key

   [Boto]
   is_secure = True
   https_validate_certificates = True


SX and import configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configuration for connecting with an SX Cluster and importing the buckets is
obtained from s3import command-line arguments. You can display their
descriptions by running ``s3import --help``.


Usage
-----

After installation, a command-line tool named ``s3import`` will become
available. Run::

   $ s3import --help

for a list of available options.
