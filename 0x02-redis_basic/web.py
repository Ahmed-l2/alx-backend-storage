#!/usr/bin/env python3
"""Module for get_page function"""
import requests
from functools import wraps
import redis

r = redis.Redis()


def url_access_count(method):
    """Decorator to count how many times a URL has been accessed"""
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:{}".format(url)
        cached_html = r.get(cached_key)
        if cached_html:
            return cached_html.decode("utf-8")

        count_key = "count:{}".format(url)
        r.incr(count_key)

        html = method(url)
        r.setex(cached_key, 10, html)
        return html
    return wrapper

@url_access_count
def get_page(url: str) -> str:
    """Obtains the HTML content of a particular URL and returns it."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
