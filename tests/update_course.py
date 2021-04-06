import unittest
import requests
import json


class TestUpdateCourse(unittest.TestCase):

    def test_successful_create_course(self):
        # When
        data = {
            "title": "Blah blah blah",
            "image_path": "images/some/path/foo.jpg",
            "price": 25.0,
            "on_discount": False,
            "discount_price": 5.0,
            "description": "New description",
            "id": 201
        }
        response = requests.put('http://localhost:5000/course/201', headers={"Content-Type": "application/json"}, data=json.dumps(data))
        # Then
        self.assertEqual(200, response.status_code)

    def test_error_course_by_id(self):
        # When
        data = {
            "title": "X",
            "image_path": "images/some/path/foo.jpg",
            "price": 25.0,
            "on_discount": "X",
            "discount_price": 5.0,
            "description": "New description",
            "id": "OOO"
        }
        response = requests.put('http://localhost:5000/course/201', headers={"Content-Type": "application/json"}, data=json.dumps(data))
        # Then
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()