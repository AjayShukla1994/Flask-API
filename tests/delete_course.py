import unittest
import requests


class TestDeleteCourseById(unittest.TestCase):

    def test_successful_course_by_id(self):
        # When
        response = requests.delete('http://localhost:5000/course/111', headers={"Content-Type": "application/json"})
        # Then
        self.assertEqual(200, response.status_code)

    def test_error_course_by_id(self):
        # When
        response = requests.delete('http://localhost:5000/course/201', headers={"Content-Type": "application/json"})
        # Then
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
