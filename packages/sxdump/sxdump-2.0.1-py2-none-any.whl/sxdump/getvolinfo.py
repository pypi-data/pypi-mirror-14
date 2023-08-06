'''
Copyright (C) 2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''
import sxclient

from configreader import ConfigReader


def get_volume_info(url):
    """
    Return a collection of volume properties.

    The collection is a result of a List Volumes operation complemented with
    volume metas from results of Locate Volume operations.
    """
    sx = create_sxcontroller(url)

    vols = sx.listVolumes.json_call().get(u'volumeList')
    for volname, voldata in vols.iteritems():
        meta = sx.locateVolume.json_call(volname, includeMeta=True).\
            get('volumeMeta')
        if meta and u'filterActive' in meta:
            uuid = meta[u'filterActive']
            try:
                meta[u'filterActive'] = \
                    sxclient.defaults.FILTER_UUID_TO_NAME[uuid]
            except KeyError:
                raise KeyError("Unknown filter UUID: {}".format(uuid))
        voldata[u'volumeMeta'] = meta
    return vols


def create_sxcontroller(url):
    """
    Create and return SXController based on the cluster configuration derived
    from the input cluster URL.
    """
    config = ConfigReader()
    username, clustername = config.parse_url(url)
    addresses = config.get_ip_addresses(clustername)
    is_secure = config.get_is_secure(clustername)
    verify_ssl_cert = True
    if is_secure:
        verify_ssl_cert = config.get_ca_path(clustername)
    port = config.get_port(clustername)
    user_key = config.get_key(clustername, username)

    cluster = sxclient.Cluster(
        clustername, addresses, is_secure=is_secure,
        verify_ssl_cert=verify_ssl_cert, port=port
    )
    user_data = sxclient.UserData.from_key(user_key)
    sx = sxclient.SXController(cluster, user_data)
    return sx
