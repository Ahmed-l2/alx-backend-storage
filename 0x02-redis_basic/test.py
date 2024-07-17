#!/usr/bin/env python3

get_page = __import__('web').get_page

result = get_page('https://google.com')

print(result)
