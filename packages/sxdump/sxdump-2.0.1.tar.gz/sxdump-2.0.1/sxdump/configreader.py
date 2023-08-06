'''
Copyright (C) 2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''
import csv
import os
import re


class ConfigReader(object):
    """
    Evaluates the files inside SX configuration directory of the current user
    and provides chosen configuration items.

    Most methods need cluster name (and sometimes user name too) as a
    parameter, both of which can be obtained from an SX cluster URL with
    parse_url method.
    """
    def __init__(self):
        self.config_dir = self.get_config_dir()

    def get_config_dir(self):
        """Return SX configuration directory path of the current user."""
        return os.path.join(os.path.expanduser('~'), '.sx')

    def parse_url(self, url):
        """
        Parse the SX cluster URL (or alias) and return username and name of the
        cluster.
        """
        if url.startswith('@'):
            with open(os.path.join(self.config_dir, '.aliases')) as aliases:
                for line in aliases:
                    alias, aliased_url = line.strip().split(None, 1)
                    if url == alias:
                        url = aliased_url
                        break
                else:
                    raise ValueError("No such alias: {}".format(url))

        url_match = re.match('^sx://([^/]*?)@?([^@/]+)$', url)
        if not url_match:
            raise ValueError("Invalid SX URL: {}".format(url))
        username, clustername = url_match.groups()
        if not username:
            username = 'default'
        return username, clustername

    def get_key(self, clustername, username):
        """Return hex-encoded user key."""
        key_path = os.path.join(self.config_dir, clustername, 'auth', username)
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        return key

    def get_ip_addresses(self, clustername):
        """Return a list of IP addresses of the cluster nodes."""
        key_path = os.path.join(self.config_dir, clustername, 'nodes')
        _, _, addresses = os.walk(key_path).next()
        return addresses

    def get_ca_path(self, clustername):
        """Return the path to CA certificate for the cluster."""
        ca_path = os.path.join(self.config_dir, clustername, 'ca.pem')
        if not os.path.isfile(ca_path):
            raise ValueError(
                "No CA certificate available under path {}".format(ca_path)
            )
        return ca_path

    def get_config_item(self, clustername, itemkey):
        """Return a configuration item from the config file."""
        config_path = os.path.join(self.config_dir, clustername, 'config')
        with open(config_path, 'rb') as config_file:
            parsed_config = csv.reader(config_file, delimiter='=')
            for key, value in parsed_config:
                if key == itemkey:
                    item = value
                    break
            else:
                item = None
        return item

    def get_is_secure(self, clustername):
        """
        Return True if the cluster connection protocol is secure (uses SSL),
        False otherwise.
        """
        config_item = self.get_config_item(clustername, 'UseSSL')
        is_secure = True if config_item == 'Yes' else False
        return is_secure

    def get_port(self, clustername):
        """Return port number user by the cluster."""
        config_item = self.get_config_item(clustername, 'HttpPort')
        port = config_item if config_item is not None else 443
        return port
