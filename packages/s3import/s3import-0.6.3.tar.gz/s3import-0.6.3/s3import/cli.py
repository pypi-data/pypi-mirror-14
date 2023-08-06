#!/usr/bin/env python
'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''
import argparse
import contextlib
import logging
import sys

import sxclient

import s3import
from s3import import S3Importer
from s3import.tools import humansize_int, positive_int

WORKER_NUMBER = 3


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Import buckets and keys from S3 to SX')
    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version=' '.join(['%(prog)s', s3import.__version__])
                        )
    parser.add_argument('-n',
                        '--name',
                        dest='cluster_name',
                        required=True,
                        help="name of the destination cluster")
    parser.add_argument('-a',
                        '--address',
                        dest='cluster_address',
                        default=None,
                        help="IP address at which the destination SX cluster "
                        "is reachable; if given, will be used instead cluster "
                        "name to connect to the cluster")
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default=None,
                        help="cluster destination port")
    parser.add_argument('-o',
                        '--owner',
                        required=True,
                        help="the volume owner")
    parser.add_argument('-k',
                        '--key-path',
                        required=True,
                        dest='key_path',
                        help="path to the file with user's authentication key")
    parser.add_argument('--no-ssl',
                        dest='is_secure',
                        action='store_false',
                        default=True,
                        help="disable secure communication "
                        "(it is enabled by default)")
    parser.add_argument('--no-verify',
                        dest='verify',
                        action='store_false',
                        default=True,
                        help="don't verify the SSL certificate")
    parser.add_argument('-r',
                        '--replica-count',
                        dest='replica_count',
                        type=positive_int,
                        required=True,
                        help="number of replicas of newly created "
                        "destination volumes")
    parser.add_argument('-s',
                        '--volume-size',
                        dest='volume_size',
                        type=humansize_int,
                        default=None,
                        help="sizes of newly created destination volumes; "
                        "allowed suffixes: K, M, G, T; if omitted, size of "
                        "every new volume will depend on the size of the "
                        "source bucket")
    parser.add_argument('--workers',
                        type=positive_int,
                        default=WORKER_NUMBER,
                        help="number of workers (threads) for importing the "
                        "keys paralelly; defaults to %(default)s")
    parser.add_argument('--volume-prefix',
                        dest='volume_prefix',
                        default=None,
                        metavar="PREFIX",
                        help="create destination volumes with names prefixed "
                        "by %(metavar)s")
    parser.add_argument('--subdir',
                        default=None,
                        metavar="SUBDIR",
                        help="copy data to a subdirectory %(metavar)s on the "
                        "destination volumes")
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help="display in detail what is being done")
    args = parser.parse_args()
    return args


def error_exit(exc):
    logger = logging.getLogger('s3import')
    msg_components = []
    msg_components.append(type(exc).__name__)
    str_exc = str(exc)
    if str_exc:
        msg_components.append(str_exc)
    msg = ': '.join(msg_components)
    logger.error(msg)
    sys.exit(1)


def setup_logging(debug=False):
    logger = logging.getLogger('s3import')
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(levelname)s (%(threadName)s): %(message)s')
    )
    logger.addHandler(handler)
    logger.addFilter(logging.Filter('s3import'))

    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logger.setLevel(level)


def main():
    args = parse_command_line()

    setup_logging(args.verbose)

    try:
        cluster = sxclient.Cluster(
            args.cluster_name, args.cluster_address, args.is_secure,
            args.verify, args.port)
        user_data = sxclient.UserData.from_key_path(args.key_path)

        with contextlib.closing(
                sxclient.SXController(cluster, user_data)) as sx:
            s3importer = S3Importer(
                volume_size=args.volume_size,
                volume_owner=args.owner,
                volume_replica=args.replica_count,
                sx=sx,
                volume_prefix=args.volume_prefix,
                subdir=args.subdir,
                worker_num=args.workers)
            s3importer.import_all()

    except (Exception, KeyboardInterrupt) as exc:
        error_exit(exc)


if __name__ == '__main__':
    main()
