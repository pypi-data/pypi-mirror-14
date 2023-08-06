'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
from functools import wraps
from xml.sax import SAXParseException

__all__ = [
    'S3ImportException', 'S3NonFatalImportError', 'S3NonFatalImportError',
    'handle_exceptions'
]


class S3ImportException(Exception):
    '''
    General exception type of s3import.
    '''


class S3FatalImportError(S3ImportException):
    '''
    Indicates that an error occured during a bucket import such that no further
    imports should be attempted.
    '''


class S3NonFatalImportError(S3ImportException):
    '''
    Indicates that an error occured during a bucket import, but other buckets
    could still be imported.
    '''


def handle_exceptions(func):
    '''Handle exceptions which can possibly be raised in multiple places.'''
    @wraps(func)
    def handled_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SAXParseException as e:
            if 'mismatched tag' in str(e):
                err_msg = (
                    'Response XML is invalid. Host or port used to connect to '
                    'S3 probably points to another service.')
                raise S3ImportException(err_msg)
    return handled_func
