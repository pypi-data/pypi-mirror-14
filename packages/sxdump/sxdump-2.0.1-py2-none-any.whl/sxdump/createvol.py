'''
Copyright (C) 2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''
import json
import sys

import sxclient

import getvolinfo

SUBCOMMAND_NAME = 'createvol'


def main(args):
    try:
        cluster_url, volname = args.url.rsplit('/', 1)
        sx = getvolinfo.create_sxcontroller(cluster_url)
        meta = json.loads(args.meta) if args.meta else None
        print create_volume(
            sx=sx, name=volname, size=args.size, replicas=args.replica,
            owner=args.owner, revisions=args.max_revisions, meta=meta
        ).json().get('requestMessage')
    except (ValueError, sxclient.exceptions.SXClientException) as exc:
        print >> sys.stderr, str(exc)
        sys.exit(1)


def create_volume(sx, name, size, replicas, owner, revisions=1, meta=None):
    resp = sx.createVolume.call(
        name, volumeSize=size, owner=owner, replicaCount=replicas,
        maxRevisions=revisions, volumeMeta=meta
    )
    return resp


def create_subparser(subparsers):
    parser = subparsers.add_parser(SUBCOMMAND_NAME)
    parser.add_argument('-s', '--size', required=True, type=int)
    parser.add_argument('-r', "--replica", required=True, type=int)
    parser.add_argument('-o', "--owner", required=True)
    parser.add_argument('-m', "--max-revisions", type=int)
    parser.add_argument("--meta")
    parser.add_argument("url", metavar="sx://[profile@]cluster/volume")
    parser.set_defaults(func=main)
