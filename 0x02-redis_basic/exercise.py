#!/usr/bin/env python3
'''Writing strings to Redis'''

from typing import Callable
import uuid
import redis


class Cache:

    def __init__(self):
        self._redis = redis.Redis()

        self._redis.flushdb()

    def store(self, data: str | bytes | int | float) -> str:
        rand_key = str(uuid.uuid4())

        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Callable):
        value = self._redis.get(key)

        return fn(value) if fn else value

    def get_str(self, key):
        return self.get(key, str)

    def get_int(self, key):
        return self.get(key, int)
