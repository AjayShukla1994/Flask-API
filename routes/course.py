"""Routes for the course resource.
"""
import json
from math import ceil
import re
from run import app
from flask import request, Response
from http import HTTPStatus
from datetime import datetime

from config import constants as c
from data import courses

def validate_data(fields):
    """ Validate all the parameters.

        Parameters
        ----------
            dict of request params

        Returns
        -------
        response : Boolean.
    """
    if ((not isinstance(fields["description"], str)) or len(fields["description"]) > 255):
        return False
    if ((not isinstance(fields["image_path"], str)) or len(fields["image_path"]) > 100):
        return False
    if (not isinstance(fields["on_discount"], bool)):
        return False
    if (not isinstance(fields["price"], float)):
        return False
    if (not isinstance(fields["discount_price"], float)):
        return False
    if ((not isinstance(fields["title"], str)) or (len(fields["image_path"]) > 100 or len(fields["image_path"]) < 5)):
        return False
    
    return True


@app.route(c.COURSE_BY_ID, methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    if int(id) in courses:
        return Response(json.dumps({
                'data': courses[int(id)]
            }), status=200)
    else:
        return Response(json.dumps({
                'messge': 'Course ' + str(id) +' does not exist'
            }), status=404)


@app.route(c.COURSE, methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    title_words = request.args.get('title-words').split(',') if request.args.get('title-words') else None
    page_number = int(request.args.get('page-number', 1))
    page_size = int(request.args.get('page-size', 10))
    if title_words == None:
        return Response(json.dumps({
                'data': [courses[id] for id in range((page_size*(page_number-1))+1, page_number*page_size+1)],
                'metadata': {
                    'page_count': ceil(200/int(page_size)),
                    'page_number': page_number,
                    'page_size': page_size,
                    'record_count': 200
                }
            }), status=200)
    else:
        searched_courses = {}
        title_word = ''
        for index in range(len(title_words)):
            title_word += title_words[index].strip()
            if index < len(title_words) - 1:
                title_word += ' | '
        course_list = [courses[i] for i in courses]
        searched_courses = list(filter(lambda i:re.search(title_word, i["title"], flags=re.IGNORECASE), course_list))
        searched_courses = sorted(searched_courses, key = lambda i: re.findall(title_word, i["title"], flags=re.IGNORECASE), reverse=True)
        return Response(json.dumps({
                'data': searched_courses[(page_size*(page_number-1))+1:page_number*page_size+1],
                'metadata': {
                    'page_count': ceil(len(searched_courses)/int(page_size)),
                    'page_number': page_number,
                    'page_size': page_size,
                    'record_count': len(searched_courses)
                }
            }), status=200)


@app.route(c.COURSE, methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    request_body = request.get_json()
    print(request_body)
    fields = {
        'description' : request_body.get('description', ""),
        'image_path' : request_body.get('image_path', ""),
        'on_discount' : request_body.get('on_discount'),
        'price' : request_body.get('price'),
        'discount_price' : request_body.get('discount_price'),
        'title' : request_body.get('title')
    }
    if validate_data(fields):
        date_created = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
        date_updated = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
        fields.update(
            {
                'date_created': date_created,
                'date_updated': date_updated
            }
        )
        max_id = max(courses.keys())
        courses[max_id+1] = fields
        courses[max_id+1].update({"id": max_id+1})
        return Response(json.dumps({
                'data': courses[int(max_id+1)]
            }), status=200)
    else:
        return Response(json.dumps({
                    'messge': 'The data does not match the payload'
                }), status=404)


@app.route(c.COURSE_BY_ID, methods=['PUT'])
def update_course(id):
    """Update a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    request_body = request.get_json()
    fields = {
        'id': int(id),
        'description' : request_body.get('description', courses[int(id)]['description']),
        'image_path' : request_body.get('image_path', courses[int(id)]['image_path']),
        'on_discount' : request_body.get('on_discount', courses[int(id)]['on_discount']),
        'price' : request_body.get('price', courses[int(id)]['price']),
        'discount_price' : request_body.get('discount_price', courses[int(id)]['discount_price']),
        'title' : request_body.get('title', courses[int(id)]['title'])
    }
    if validate_data(fields):
        date_updated = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
        fields.update(
            {
                'date_created': courses[int(id)]['date_created'],
                'date_updated': date_updated
            }
        )
        courses[id] = fields
        return Response(json.dumps({
                'data': courses[int(id)]
            }), status=200)
    else:
        return Response(json.dumps({
                'messge': 'The id does match the payload'
            }), status=404)


@app.route(c.COURSE_BY_ID, methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    if int(id) in courses:
        del courses[int(id)]
        return Response(json.dumps({
                'messge': 'The specified course was deleted'
            }), status=200)
    else:
        return Response(json.dumps({
                'messge': 'Course ' + str(id) +' does not exist'
            }), status=404)
