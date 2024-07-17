#!/usr/bin/env python3
"""Module for get_page function"""
import requests
from functools import wraps
import redis

r = redis.Redis()


def url_access_count(method):
    @wraps(method)
    def wrapper(url):
        # Track access count (increment Redis key)
        count_key = f"count:{url}"
        r.incr(count_key)

        # Retrieve or fetch HTML content
        cached_key = f"cached:{url}"
        cached_html = r.get(cached_key)
        if cached_html:
            return cached_html.decode("utf-8")

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
    test_url = "http://slowwly.robertomurray.co.uk"
    html_content = get_page(test_url)
    print(html_content)
