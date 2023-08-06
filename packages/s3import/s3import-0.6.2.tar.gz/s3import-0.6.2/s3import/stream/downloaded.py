'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
from tempfile import SpooledTemporaryFile

__all__ = ['DownloadedFileStream']


class DownloadedFileStream(object):
    '''
    Mock-stream interface for boto.s3.key.Key.

    Upon initialization, the whole key's content is retrieved and stored in a
    temporary file. Afterwards DownloadedFileStream acts as a proxy interface
    of the underlying temporary file (i.e. 'read', 'write' and other stream
    methods are run on the tempfile).
    '''

    def __init__(self, s3key, max_mem=0):
        self.key = s3key
        self.max_mem = max_mem
        self._stream = SpooledTemporaryFile(max_size=self.max_mem)
        self.key.get_contents_to_file(self._stream)
        self._stream.seek(0)

    def __getattr__(self, name):
        return getattr(self._stream, name)
