#!/usr/bin/env python3
"""Module for list_all"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    return mongo_collection.find()
