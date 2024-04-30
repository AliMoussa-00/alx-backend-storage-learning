#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
    
    print(f'xx=> {cache.get(key, fn)} \t|| {type(cache.get(key, fn))}')
    print(f'zz=> {cache.get_str(key)} \t|| {type(cache.get_str(key))}')
    # print(f'zz=> {cache.get_str(key)} \t|| {type(cache.get_int(key))}')
    print()
