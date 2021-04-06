import unittest
import requests
import json


class TestCreateCourse(unittest.TestCase):

    def test_successful_create_course(self):
        # When
        data = {
            "title" : "Brand new course",
            "image_path" : "images/some/path/foo.jpg",
            "price" : 25.0,
            "on_discount" : False,
            "discount_price" : 5.0,
            "description" : "This is a brand new course"
        }
        response = requests.post('http://localhost:5000/course', headers={"Content-Type": "application/json"}, data=json.dumps(data))
        # Then
        self.assertEqual(200, response.status_code)

    def test_error_course_by_id(self):
        data = {
            "title" : "X",
            "image_path" : "images/some/path/foo.jpg",
            "price" : 12.0,
            "on_discount" : False,
            "discount_price" : 5.0,
            "description" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
        response = requests.post('http://localhost:5000/course', headers={"Content-Type": "application/json"}, data=json.dumps(data))
        # Then
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
