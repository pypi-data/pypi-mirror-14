import json

try:
    from pymemcache.client.base import Client
except ImportError as e:
    raise ImportError('Failed to import "pymemcache" ({})'.format(e))

from .abstract import Abstract
from .abstract import NotSupported

def get_default_client(server_config = None):
    return Client(
        server_config or ('127.0.0.1', 11211),
        serializer   = serializer,
        deserializer = deserializer
    )

def serializer(key, value):
    if type(value) == str:
        return value, 1

    return json.dumps(value), 2

def deserializer(key, value, flags):
    actual_value = value.decode('utf-8')

    if flags == 1:
        return actual_value

    elif flags == 2:
        return json.loads(actual_value)

    raise Exception("Unknown serialization format")

class Memcached(Abstract):
    def __init__(self, storage = None, namespace = None):
        self._storage   = storage
        self._namespace = namespace or ''

    def get(self, key):
        actual_key = self._actual_key(key)

        return self._storage.get(actual_key)

    def set(self, key, value):
        actual_key = self._actual_key(key)

        self._storage.set(actual_key, value)

    def remove(self, key):
        actual_key = self._actual_key(key)

        self._storage.delete(actual_key)

    def find(self, *args, **kwargs):
        raise NotSupported()

    def _actual_key(self, key):
        if not self._namespace:
            return key

        return '{}-{}'.format(self._namespace, key)
