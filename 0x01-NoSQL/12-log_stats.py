#!/usr/bin/env python3
import pymongo
"""Module for log_stats"""


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

    print(f"{len(list(nginx.find()))} logs")
    print("Methods:")
    print(f"\t method GET: {GET}")
    print(f"\t method POST: {POST}")
    print(f"\t method PUT: {PUT}")
    print(f"\t method PATCH: {PATCH}")
    print(f"\t method DELETE: {DELETE}")
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
