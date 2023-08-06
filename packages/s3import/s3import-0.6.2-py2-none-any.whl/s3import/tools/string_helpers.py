'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
import posixpath
import re

__all__ = ['toutf8', 'join_posix_paths']


def toutf8(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    elif isinstance(text, str):
        return text.decode('utf-8').encode('utf-8')
    else:
        raise TypeError(
            "Object is neither 'str' nor 'unicode': {}".format(repr(text))
        )


def join_posix_paths(*paths):
    double_dot_in_paths = any(
        re.search(r'(^|/)\.\.(/|$)', path) for path in paths
    )
    if double_dot_in_paths:
        raise ValueError("Path with '..' is not allowed")

    unslashed = (path.lstrip('/') for path in paths)
    normalized = (posixpath.normpath(path) for path in unslashed)
    joined = posixpath.join(*normalized)
    return joined
