"""Dogpile backend implementation for PyMemcache and AWS Elasticache.

Inspired from https://bitbucket.org/zzzeek/dogpile.cache/pull-requests/34
"""

from dogpile.cache.backends.memcached import GenericMemcachedBackend

from .cluster import get_cluster_info


pymemcache = None


class ConfigError(RuntimeError):
    pass


class ClusterDiscoveryError(RuntimeError):
    pass


def asbool(value):
    value = str(value).lower()
    if value == 'true':
        return True
    if value in 'false':
        return False
    raise ValueError('Invalid value for boolean: %s' % value)


class ElasticachePyMemcacheBackend(GenericMemcachedBackend):
    """A backend for the pymemcache memcached client.

    PyMemcache: https://github.com/pinterest/pymemcache

    This is a pure Python memcached client which includes consistent hashing
    and connection pooling.

    A typical configuration::

        from dogpile.cache import make_region

        region = make_region().configure(
            'elasticache_pymemcache',
            expiration_time = 3600,
            arguments = {
                'configuration.host': '54.43.32.21',
                'configuration.port': '11211',
            }
        )

    The full default configuration::

        from dogpile.cache import make_region

        region = make_region().configure(
            'elasticache_pymemcache',
            expiration_time = 3600,
            arguments = {
                'configuration.host': '54.43.32.21',
                'configuration.port': '11211',
                'serializer': pymemcache.serde.python_memcache_serializer,
                'deserializer': pymemcache.serde.python_memcache_deserializer,
                'no_delay': True,
                'connect_timeout': 1,
                'timeout': 1,
                'retry_attempts': 2,
                'retry_timeout': 1,
                'dead_timeout': 60,
                'use_pooling': True,
                'ignore_exc': True,
            }
        )
    """

    def _imports(self):
        global pymemcache
        import pymemcache  # noqa
        from pymemcache.client import base, hash  # noqa
        from pymemcache import serde  # noqa

    def __init__(self, arguments):
        self._imports()

        self.client_cls = pymemcache.client.hash.HashClient

        try:
            self.serializer = arguments.get('serializer', False)
            self.deserializer = arguments.get('deserializer', False)
            self.no_delay = asbool(arguments.get('no_delay', True))
            self.connect_timeout = float(arguments.get('connect_timeout', 1))
            self.timeout = float(arguments.get('timeout', 1))
            self.retry_attempts = int(arguments.get('retry_attempts', 2))
            self.retry_timeout = int(arguments.get('retry_timeout', 1))
            self.dead_timeout = int(arguments.get('dead_timeout', 60))
            self.use_pooling = asbool(arguments.get('use_pooling', True))
            self.ignore_exc = asbool(arguments.get('ignore_exc', True))
        except ValueError as err:
            raise ConfigError("Configuration error: %s" % err)

        try:
            self.config_host = arguments['configuration.host']
            self.config_port = arguments['configuration.port']
        except KeyError:
            raise ConfigError("Elasticache configuration endpoint is missing")

        self.hosts = self.get_hosts()

        arguments['url'] = ''  # GenericMemcachedBackend expects this
        super(ElasticachePyMemcacheBackend, self).__init__(arguments)

    def get_hosts(self):
        try:
            info = get_cluster_info(self.config_host, self.config_port)
        except:
            raise ClusterDiscoveryError("Failed to get cluster nodes")

        hosts = info['nodes']
        return hosts

    def _create_client(self):

        serializer = (pymemcache.serde.python_memcache_serializer
                      if self.serializer is False else self.serializer)
        deserializer = (pymemcache.serde.python_memcache_deserializer
                        if self.deserializer is False else self.deserializer)

        client = self.client_cls(self.hosts,
                                 no_delay=self.no_delay,
                                 connect_timeout=self.connect_timeout,
                                 timeout=self.timeout,
                                 retry_attempts=self.retry_attempts,
                                 retry_timeout=self.retry_timeout,
                                 dead_timeout=self.dead_timeout,
                                 use_pooling=self.use_pooling,
                                 ignore_exc=self.ignore_exc,
                                 serializer=serializer,
                                 deserializer=deserializer)
        return client
