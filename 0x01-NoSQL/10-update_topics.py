#!/usr/bin/env python3
"""Module for update_topics"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name"""

    filter = {"name": name}
    update = {"$set": {"topics": topics}}

    mongo_collection.update_many(filter, update)
