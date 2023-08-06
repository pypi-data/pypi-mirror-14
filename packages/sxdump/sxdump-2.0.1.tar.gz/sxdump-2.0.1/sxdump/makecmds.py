'''
Copyright (C) 2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

Print commands to recreate users, volumes and ACL on a new SX cluster
'''
import argparse
import json
import sys
import pipes
import re
import os
import stat
from subprocess import CalledProcessError, Popen, PIPE

from . import __version__
from getvolinfo import get_volume_info

SUBCOMMAND_NAME = 'makecmds'

SXLS = 'sxls'
SXACL = 'sxacl'
SXVOL = 'sxvol'
SXCP = 'sxcp'
SXADM = 'sxadm'


def create_subparser(subparsers):
    parser = subparsers.add_parser(
        SUBCOMMAND_NAME,
        usage='sxdump [-h] [-V] -b BACKUP_DIR sx://[profile@]cluster',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Print commands to recreate users, "
                    "volumes and ACL on a new SX cluster",
        epilog="Running this tool will generate two scripts"
        " in the current directory:\n"
        " sx-backup.sh: backs up sx://cluster to BACKUPDIR\n"
        " sx-restore.sh: recreates users,volumes,acls restores BACKUPDIR\n"
    )
    parser.add_argument('-V', '--version', action='version',
                        version="sxdump {}".format(__version__))
    parser.add_argument('-b', "--backup-dir", required=True,
                        help="destination directory for cluster backup")
    parser.add_argument("cluster", metavar="sx://[profile@]cluster",
                        help="specifies the cluster to backup")
    parser.set_defaults(func=main)


def check_output(cmd):
    """ like subprocess.check_output, for python2.6 compatibility """
    process = Popen(cmd, stdout=PIPE)
    output = process.communicate()[0]
    retcode = process.poll()
    if retcode:
        raise CalledProcessError(retcode, cmd, output=output)
    return output


def try_subcommands(main, subcmds):
    """ Try to guess which subcommand the main command supports """
    for subcmd in subcmds:
        try:
            cmdhelp = check_output([main, subcmd, "--help"])
            if "Usage: %s %s" % (os.path.basename(SXACL), subcmd) in cmdhelp:
                return subcmd
        except CalledProcessError:
            continue
    print >> sys.stderr, "Unknown sxacl command version"
    sys.exit(2)


def get_version(cmd):
    """ Retrieve version number of a tool """
    try:
        return check_output([cmd, "-V"]).split(" ")[1]
    except OSError as exc:
        print >> sys.stderr, "Failed to execute '%s': %s" % (cmd, exc)
        sys.exit(1)


def check_versions(commands):
    """ Ensure that all the commands are the same version """
    versions = set([get_version(cmd) for cmd in commands])
    if len(versions) > 1:
        print >> sys.stderr, "Tool version mismatch: ", list(versions)
        sys.exit(1)

check_versions([SXLS, SXACL, SXVOL, SXCP, SXADM])
SXACL_LIST = try_subcommands(SXACL, ['volshow', 'show', 'list'])


def print_shell(dest, lst):
    """ Print properly quoted shell commands """
    dest.write(" ".join([pipes.quote(s) for s in lst]) + "\n")


def print_progress(dest, msg):
    """ Echo a message separated by newlines """
    print_shell(dest, ["echo"])
    print_shell(dest, ["echo", msg])
    print_shell(dest, ["echo"])


def create_users(sxurl):
    """ Print commands to create SX users """
    lines = check_output([SXACL, "userlist", "--verbose", sxurl]).\
        rstrip().split('\n')
    print_progress(new, "Creating users")
    pattern = re.compile(r"^(?P<user>\S+) *"
                         r"(role:(?P<role>\w+)) *"
                         r"(quota:(?P<quota>\S+)) *"
                         r"(desc:(?P<desc>.*))")

    for line in lines:
        match = pattern.search(line)
        if match is None:
            print >> sys.stderr, "WARNING: Cannot parse sxacl output: " + line
            continue
        user = match.group('user')
        if user == 'admin':
            continue
        cmd = [SXACL, "useradd", "--role", match.group('role')]
        quota = match.group('quota')
        if quota != 'unlimited':
            cmd.extend(["--quota", quota.split('/')[1]])
        desc = match.group('desc')
        if desc != '':
            cmd.extend(["--desc", desc])

        token = check_output([SXACL, "usergetkey", user, sxurl]).strip()
        cmd.extend([user, sxurl, "--force-key", token])
        print_shell(new, cmd)


def set_cluster_meta(sxurl):
    """ Print commands to set cluster meta """
    try:
        kvs = check_output([SXADM, "cluster", "--get-meta=ALL", sxurl]).\
            rstrip().split('\n')
    except CalledProcessError:
        print >> sys.stderr, "WARNING: Can't obtain cluster meta"
    else:
        print_progress(new, "Setting cluster meta")
        for kv in kvs:
            print_shell(new, [SXADM, "cluster", "--set-meta", kv, sxurl])


def update_cluster_settings(sxurl):
    """ Print commands to update cluster settings """
    if int(get_version(SXADM).split(".")[0]) >= 2:
        try:
            kvs = check_output([SXADM, "cluster", "--get-param=ALL", sxurl]).\
                rstrip().split('\n')
        except CalledProcessError:
            print >> sys.stderr, "WARNING: Can't obtain cluster settings"
        else:
            print_progress(new, "Updating cluster settings")
            for kv in kvs:
                if kv.split('=')[0] == "sxsetup_conf":
                    continue
                print_shell(new, [SXADM, "cluster", "--set-param", kv, sxurl])


def list_acl(sxurl):
    """ Retrieve the ACL of a volume """
    lines = check_output([SXACL, SXACL_LIST, sxurl]).rstrip().split('\n')
    owner = None
    read_acl = []
    write_acl = []
    manager_acl = []
    admin_acl = []
    firstuser = None
    for line in lines:
        user, allprivs = line.split(": ", 1)
        if user == '(all admin users)':
            continue
        privs = allprivs.split(" ")
        if firstuser is None:
            firstuser = user
        if 'owner' in privs:
            owner = user
        if 'admin' in privs:
            admin_acl.append(user)
        if 'read' in privs:
            read_acl.append(user)
        if 'write' in privs:
            write_acl.append(user)
        if 'manager' in privs:
            manager_acl.append(user)
    # if owner is admin old sx versions don't always list owner priv
    if owner is None:
        owner = firstuser
    return owner, read_acl, write_acl, manager_acl, admin_acl


def create_volumes(sxurl):
    """ Print commands to create SX volumes and set ACLs """
    volinfo = get_volume_info(sxurl)
    volumes = []
    print_progress(new, "Creating volumes")
    for name, properties in volinfo.iteritems():
        url = '/'.join([sxurl, name])
        owner, read_acl, write_acl, manager_acl, admin_acl = list_acl(url)
        cmd = [
            "sxdump",
            "createvol",
            "--owner", owner,
            "--replica", str(properties.get('replicaCount')),
            "--size", str(properties.get('sizeBytes')),
            "--max-revisions", str(properties.get('maxRevisions')),
            url
        ]
        meta = properties.get('volumeMeta')
        if meta:
            metastr = json.dumps(meta)
            cmd.extend(['--meta', metastr])
            volfilter = meta.get('filterActive')
        else:
            volfilter = None

        if volfilter == 'aes256' or volfilter == 'aes256_old':
            print >> sys.stderr, ("\nWARNING: "
                                  "Skipping encrypted volume '%s'\n" % url)
            continue
        if name.startswith("libres3-"):
            print >> sys.stderr, ("Skipping "
                                  "LibreS3 temporary volume '%s'" % url)
            continue
        volumes.append(url)
        if name == '_sxsetup.conf':
            print >> sys.stderr, ("Skipping "
                                  "sxsetup configuration volume '%s'" % name)
            continue

        new.write("# volume '%s'\n" % name)
        print_shell(new, cmd)

        for user in read_acl:
            if user == owner or user in admin_acl or user == 'admin':
                continue
            print_shell(new, [SXACL, "volperm", "--grant=read", user, url])
        for user in write_acl:
            if user == owner or user in admin_acl or user == 'admin':
                continue
            print_shell(new, [SXACL, "volperm", "--grant=write", user, url])
        for user in manager_acl:
            if user == owner or user in admin_acl or user == 'admin':
                continue
            print_shell(new, [SXACL, "volperm", "--grant=manager", user, url])
            if user not in read_acl:
                print_shell(
                    new, [SXACL, "volperm", "--revoke=read", user, url])
            if user not in write_acl:
                print_shell(
                    new, [SXACL, "volperm", "--revoke=write", user, url])
        if owner not in read_acl:
            print_shell(new, [SXACL, "volperm", "--revoke=read", owner, url])
        if owner not in write_acl:
            print_shell(new, [SXACL, "volperm", "--revoke=write", owner, url])
        new.write("\n")
    for volurl in volumes:
        vol = volurl.rsplit("/", 1)[1]
        print_progress(old, "Backing up volume %s" % volurl)
        localdir = "%s/%s" % (BACKUPDIR, vol)
        print_shell(old, ["mkdir", "-m", "0700", "-p", localdir])
        print_shell(old, [SXCP, "-r", volurl, localdir])
        if vol == '_sxsetup.conf':
            print >> sys.stderr, ("Skipping "
                                  "sxsetup configuration volume '%s'" % vol)
            continue
        print_progress(new, "Restoring volume %s" % volurl)
        print_shell(new, [SXCP, "-r", localdir + "/", volurl + "/"])


def main(args):
    global OLD, NEW, BACKUPDIR
    global old, new
    OLD = 'sx-backup.sh'
    NEW = 'sx-restore.sh'
    BACKUPDIR = args.backup_dir

    os.umask(0o77)
    with open(OLD, 'w') as old:
        with open(NEW, 'w') as new:
            print "Generating %s and %s" % (OLD, NEW)
            new.write("#! /bin/sh\n"
                      "set -e\n")
            old.write("#! /bin/sh\n"
                      "set -e\n")
            print_shell(old, ["mkdir", "-m", "0700", "-p", BACKUPDIR])
            create_users(args.cluster)
            create_volumes(args.cluster)
            set_cluster_meta(args.cluster)
            update_cluster_settings(args.cluster)
            os.chmod(OLD, stat.S_IRWXU)
            os.chmod(NEW, stat.S_IRWXU)
            print "Review %s (uncomment/edit paths as necessary)" % OLD
            print "Run %s on the old cluster" % OLD
            print "Review %s (uncomment/edit paths as necessary)" % NEW
            print "Stop old cluster"
            print "Use sxsetup --config-file to setup the new cluster"
            print "Run %s on the new cluster" % NEW
