'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
import io

__all__ = ['ChunkedStream']


class ChunkedStream(io.IOBase):
    '''
    Mock-stream interface for boto.s3.key.Key.

    ChunkedStream.read(bytes) iterates over the key only until it gets the
    amount of key's content needed to return the amount of bytes specified by
    'bytes'.
    '''

    def __init__(self, s3key):
        self.key = s3key
        self._remaining = ''
        self._is_exhausted = False

    def read(self, bytes=None):
        if bytes is not None and not isinstance(bytes, (int, long)):
            print bytes
            raise ValueError(
                "Integer argument expected, got '%s'." %
                bytes.__class__.__name__
            )

        if bytes is None or bytes < 0:
            return self.readall()
        elif bytes == 0:
            return ''
        else:
            return self._read_bytes(bytes)

    def readall(self):
        if self._is_exhausted:
            remaining, self._remaining = self._remaining, ''
            return remaining

        stream = io.BytesIO(self._remaining)
        self._remaining = ''
        stream.seek(0, io.SEEK_END)

        for chunk in self.key:
            stream.write(chunk)

        self._is_exhausted = True

        stream.seek(0)
        return stream.read()

    def _read_bytes(self, bytes):
        if self._is_exhausted:
            returned, self._remaining = (
                self._remaining[:bytes], self._remaining[bytes:]
            )
            return returned

        stream = io.BytesIO(self._remaining)
        self._remaining = ''
        stream.seek(0, io.SEEK_END)

        while bytes > stream.tell():
            try:
                chunk = next(self.key)
                stream.write(chunk)
            except StopIteration:
                # after raising StopIteration, key.next() starts from the
                # beginning, breaking the iterator protocol; therefore,
                # reading after StopIteration is handled differently.
                self._is_exhausted = True
                break

        stream.seek(bytes)
        self._remaining = stream.read()
        stream.seek(0)
        return stream.read(bytes)

    def write(self, *args, **kwargs):
        raise NotImplementedError
