"""Routines associated with the application data.
"""
import json

courses = {}


def load_data():
    """
        Load the data from the json file into
        In memory data structure.
    """
    file = open('json/course.json')
    for json_data in json.load(file):
        id = json_data['id']
        courses[id] = json_data
