'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
import logging

from requests.packages import urllib3

from importer import S3Importer
from contexts import S3ConnectionContext
from exceptions import S3ImportException

__version__ = '0.6.2'

__all__ = ['S3Importer', 'S3ConnectionContext', 'S3ImportException']

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
