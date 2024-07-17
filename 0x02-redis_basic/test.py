#!/usr/bin/env python3
import redis
get_page = __import__('web').get_page

r = redis.Redis()

url = 'http://google.com'
print(get_page(url))
print(r.get(f"count:{url}"))