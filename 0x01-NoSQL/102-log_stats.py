#!/usr/bin/env python3
"""Module for log_stats"""
import pymongo


def log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    logs = myclient["logs"]
    nginx = logs["nginx"]

    GET = len(list(nginx.find({"method": "GET"})))
    POST = len(list(nginx.find({"method": "POST"})))
    PUT = len(list(nginx.find({"method": "PUT"})))
    PATCH = len(list(nginx.find({"method": "PATCH"})))
    DELETE = len(list(nginx.find({"method": "DELETE"})))
    status_check = len(list(nginx.find({"method": "GET", "path": "/status"})))

    print("{} logs".format(len(list(nginx.find()))))
    print("Methods:")
    print("\tmethod GET: {}".format(GET))
    print("\tmethod POST: {}".format(POST))
    print("\tmethod PUT: {}".format(PUT))
    print("\tmethod PATCH: {}".format(PATCH))
    print("\tmethod DELETE: {}".format(DELETE))
    print("{} status check".format(status_check))

    ip = {}
    objects = list(nginx.find())

    for obj in objects:
        if obj.get('ip') in ip:
            ip[obj.get('ip')] += 1
        else:
            ip[obj.get('ip')] = 1

    sorted_ips = sorted(ip.items(), key=lambda item: item[1],
                        reverse=True)[:10]

    print("IPs:")
    for key, value in sorted_ips:
        print("\t{}: {}".format(key, value))


if __name__ == "__main__":
    log_stats()
