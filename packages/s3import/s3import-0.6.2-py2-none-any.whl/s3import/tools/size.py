'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''

__all__ = ['calculate_volume_size']


SIZE_MULTIPLIER = 1.1
MINIMAL_VOLUME_SIZE = 1048576


def calculate_volume_size(required_space):
    return max(int(required_space * SIZE_MULTIPLIER), MINIMAL_VOLUME_SIZE)
