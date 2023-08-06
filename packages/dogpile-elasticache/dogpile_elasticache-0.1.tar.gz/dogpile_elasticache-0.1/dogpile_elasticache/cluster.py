"""Utils for discovery cluster.

Almost entirely copied from https://github.com/gusdan/django-elasticache
"""

from distutils.version import StrictVersion
import re
from telnetlib import Telnet


class WrongProtocolData(ValueError):
    """Got something unexpected in telnet protocol."""

    def __init__(self, cmd, response):
        super(WrongProtocolData, self).__init__(
            'Unexpected response {} for command {}'.format(response, cmd))


def get_cluster_info(host, port, timeout=10):
    """Get nodes list using the Elasticache configuration endpoint.

    Returns:
        dict like {'nodes': ['IP:port'], 'version': '1.4.4'}
    """
    client = Telnet(host, int(port))
    client.write(b'version\n')
    res = client.read_until(b'\r\n', timeout=timeout).strip()
    version_list = res.split(b' ')
    if len(version_list) != 2 or version_list[0] != b'VERSION':
        raise WrongProtocolData('version', res)
    version = version_list[1]
    if StrictVersion(str(version)) >= StrictVersion('1.4.14'):
        cmd = b'config get cluster\n'
    else:
        cmd = b'get AmazonElastiCache:cluster\n'
    client.write(cmd)
    res = client.read_until(b'\n\r\nEND\r\n', timeout=timeout)
    client.close()
    ls = list(filter(None, re.compile(br'\r?\n').split(res)))
    if len(ls) != 4:
        raise WrongProtocolData(cmd, res)

    try:
        version = int(ls[1])
    except ValueError:
        raise WrongProtocolData(cmd, res)

    nodes = []
    try:
        for node in ls[2].split(b' '):
            host, ip, port = node.split(b'|')
            nodes.append((str(ip or host), int(port)))
    except ValueError:
        raise WrongProtocolData(cmd, res)
    return {
        'version': version,
        'nodes': nodes
    }
