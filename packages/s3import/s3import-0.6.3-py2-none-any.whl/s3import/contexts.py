'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''


class S3ConnectionContext(object):
    host = None
    port = None
    access_key_id = None
    secret_access_key = None
    is_secure = True
    validate_certs = True

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
