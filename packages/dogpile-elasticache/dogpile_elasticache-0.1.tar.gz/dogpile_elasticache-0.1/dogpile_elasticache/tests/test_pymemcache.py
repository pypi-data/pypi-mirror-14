import unittest

from nose.tools import raises
import mock

from dogpile_elasticache.backends import (
    ConfigError,
    ClusterDiscoveryError,
    ElasticachePyMemcacheBackend)
import pymemcache.client.hash


@mock.patch('dogpile_elasticache.backends.get_cluster_info')
class Test(unittest.TestCase):

    ARGS = {
        'configuration.host': 'host',
        'configuration.port': 'port',
    }

    @raises(ConfigError)
    def test_no_arguments(self, m_get_cluster_info):
        ElasticachePyMemcacheBackend({})

    def test_init(self, m_get_cluster_info):
        m_get_cluster_info.return_value = {'nodes': 'NODES'}

        backend = ElasticachePyMemcacheBackend(self.ARGS)

        m_get_cluster_info.assert_called_once_with('host', 'port')
        self.assertEqual(backend.hosts, 'NODES')

    @raises(ConfigError)
    def test_invalid_no_delay(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['no_delay'] = 'not a bool'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_connect_timeout(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['connect_timeout'] = 'not an float'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_timeout(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['timeout'] = 'not an float'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_retry_attempts(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['retry_attempts'] = 'not an int'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_retry_timeout(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['retry_timeout'] = 'not an int'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_dead_timeout(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['dead_timeout'] = 'not an int'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_use_pooling(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['use_pooling'] = 'not an bool'
        ElasticachePyMemcacheBackend(args)

    @raises(ConfigError)
    def test_invalid_ignore_exc(self, m_get_cluster_info):
        args = self.ARGS.copy()
        args['ignore_exc'] = 'not an bool'
        ElasticachePyMemcacheBackend(args)

    @raises(ClusterDiscoveryError)
    def test_cluster_info_failed(self, m_get_cluster_info):
        m_get_cluster_info.side_effect = Exception()

        ElasticachePyMemcacheBackend(self.ARGS)

    def test_create_client(self, m_get_cluster_info):
        m_get_cluster_info.return_value = {'nodes': [('127.0.0.1', 11211)]}

        backend = ElasticachePyMemcacheBackend(self.ARGS)

        client = backend._create_client()
        self.assertIsInstance(client, pymemcache.client.hash.HashClient)

        self.assertEqual(client.clients.keys(), ['127.0.0.1:11211'])
