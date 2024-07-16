#!/usr/bin/env python3
"""Module for top_students"""
import pymongo



def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    students = list(mongo_collection.find())
    for student in students:
        topics = student['topics']
        average_score = sum(topic['score'] for topic in topics) / len(topics)
        student['averageScore'] = average_score

    return sorted(students, key=lambda x: x['averageScore'], reverse=True)
