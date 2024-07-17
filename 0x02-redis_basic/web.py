#!/usr/bin/env python3
"""Module for get_page function"""
import requests
from functools import wraps
import redis

r = redis.Redis()


def url_access_count(method):
    """Decorator to monitor access to URL."""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        count_key = f"count:{url}"
        r.incr(count_key)

        cached_key = f"cached:{url}"
        cached_html = r.get(cached_key)
        if cached_html:
            return cached_html.decode("utf-8")

        html = method(url)
        r.set(cached_key, html, 10)
        return method(*args, **kwargs)

    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Obtains the HTML content of a URL and returns it."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text
