#!/usr/bin/env python3
"""Module for Cache Class"""
import redis
from typing import Union, Callable
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    inputs = "{}:inputs".format(method.__qualname__)
    outputs = "{}:outputs".format(method.__qualname__)

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> \
            Union[int, str, float, bytes, None]:
        value = self._redis.get(key)
        if fn is None:
            return value
        if value is None:
            return None
        return fn(value)

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, int)


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    key = method.__qualname__
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")

    input_key = "{}:inputs".format(key)
    output_key = "{}:outputs".format(key)

    inputs = redis.lrange(input_key, 0, -1)
    outputs = redis.lrange(output_key, 0, -1)

    results = list(zip(inputs, outputs))

    print("{} was called {} times:".format(key, count))

    for i, o in results:
        print("{}(*{}) -> {}".format(key, i.decode('utf-8'),
                                     o.decode('utf-8')))
