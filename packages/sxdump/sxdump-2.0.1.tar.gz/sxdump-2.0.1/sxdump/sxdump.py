'''
Copyright (C) 2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

Print commands to recreate users, volumes and ACL on a new SX cluster
'''
import argparse
import sys

from . import __version__
import createvol
import makecmds


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version',
                        version="%(prog)s {}".format(__version__))

    subparsers = parser.add_subparsers()
    createvol.create_subparser(subparsers)
    makecmds.create_subparser(subparsers)

    return parser


def main():
    if len(sys.argv) == 1 or sys.argv[1] != createvol.SUBCOMMAND_NAME:
        sys.argv.insert(1, makecmds.SUBCOMMAND_NAME)
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
