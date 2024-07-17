#!/usr/bin/env python3
"""Module for Cache Class"""
import redis
from typing import Union, Optional, Callable, Any
import uuid
from functools import wraps


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
