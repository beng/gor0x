import pickle
import json

from redis import Redis


class Cache(object):
    def __init__(self, serial=pickle, prefix=None, db=10):
        self.conn = Redis(db=db)
        self.prefix = prefix
        self.serial = serial
        self.flush = self.conn.flushdb

    def _make_key(self, key):
        if self.prefix:
            key = '%s:%s' % (self.prefix, key)

        return key

    def _unserialize(self, val):
        return self.serial.loads(val)

    def _serialize(self, val):
        return self.serial.dumps(val)

    def hget(self, key, field):
        key = self._make_key(key)
        return self._unserialize(self.conn.hget(key, field))

    def hset(self, key, field, val):
        key = self._make_key(key)
        return self.conn.hset(key, field, self._serialize(val))

    def hgetall(self, name):
        return self.conn.hgetall(name)

    def hmget(self, name, key, *args):
        return self.conn.hmget(name, key, *args)

    def hmset(self, name, mapping):
        return self.conn.hmset(name, mapping)

    def hkeys(self, name):
        return self.conn.hkeys(name)