#!/usr/bin/env python3
'''Writing strings to Redis'''

from functools import wraps
from typing import Any, Callable, Optional, Union
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called
    and increments the count in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Union[str, bytes, int, float]:
        """
        Wrapper function that increments the count of method called.
        """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)

        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function to store the method history
        """
        func_name = method.__qualname__

        if isinstance(self._redis, redis.Redis):
            for arg in args:
                self._redis.rpush(f'{func_name}:inputs', str(arg))

        output = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(f'{func_name}:outputs', str(output))

        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    function to display the history of calls of a particular function.
    """

    if method is None or not hasattr(method, '__self__'):
        return

    r = method.__self__._redis
    if not isinstance(r, redis.Redis):
        return

    func_name = method.__qualname__
    print(f'{func_name} was called {int(r.get(func_name))} times:')

    input_list = r.lrange(f'{func_name}:inputs', 0, -1)
    output_list = r.lrange(f'{func_name}:outputs', 0, -1)
    for input, output in zip(input_list, output_list):
        print('{}(*({},)) -> {}'.format(
            func_name,
            input.decode("utf-8"),
            output.decode("utf-8")
        ))


class Cache:
    """
    A class representing Redis storage with functionality
    to store and retrieve data.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache object.
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in the cache and returns a unique key for retrieval.
        """

        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves the value associated with the given key from the cache.
        """

        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """
        Retrieves the value associated with the given key
        from the cache and converts it to a string.
        """

        return self.get(key, str)

    def get_int(self, key) -> int:
        """
        Retrieves the value associated with the given key
        from the cache and converts it to an integer.
        """

        return self.get(key, int)
