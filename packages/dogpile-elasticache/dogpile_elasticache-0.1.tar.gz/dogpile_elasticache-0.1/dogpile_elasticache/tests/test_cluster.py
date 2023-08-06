from mock import patch, call, MagicMock
from nose.tools import eq_, raises
from dogpile_elasticache.cluster import get_cluster_info, WrongProtocolData


TEST_PROTOCOL_1 = [
    b'VERSION 1.4.14',
    b'CONFIG cluster 0 138\r\n1\nhost|ip|11211 host||11211\n\r\nEND\r\n',
]

TEST_PROTOCOL_2 = [
    b'VERSION 1.4.13',
    b'CONFIG cluster 0 138\r\n1\nhost|ip|11211 host||11211\n\r\nEND\r\n',
]


@patch('dogpile_elasticache.cluster.Telnet')
def test_happy_path(telnet):
    client = telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_1
    info = get_cluster_info('', 0)
    eq_(info['version'], 1)
    eq_(info['nodes'], [('ip', 11211), ('host', 11211)])


@raises(WrongProtocolData)
@patch('dogpile_elasticache.cluster.Telnet', MagicMock())
def test_bad_protocol():
    get_cluster_info('', 0)


@patch('dogpile_elasticache.cluster.Telnet')
def test_last_versions(telnet):
    client = telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_1
    get_cluster_info('', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'config get cluster\n'),
    ])


@patch('dogpile_elasticache.cluster.Telnet')
def test_prev_versions(telnet):
    client = telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_2
    get_cluster_info('', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'get AmazonElastiCache:cluster\n'),
    ])
