'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
# Since version 2.7.9, SSL certificates are verified by default in Python's
# standard library modules (see PEP 476). Boto does its own verification and
# settings from boto config file do not influence stdlib's modules behaviour.
# Therefore, SSL verification in the standard library modules is turned off
# here, leaving it to boto.

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
