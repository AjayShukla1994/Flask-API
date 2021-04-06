import unittest
import requests


class TestGetCourse(unittest.TestCase):

    def test_default_page_courses(self):
        # When
        response = requests.get('http://localhost:5000/course', headers={"Content-Type": "application/json"})
        # Then
        self.assertEqual(200, response.status_code)

    def test_nth_page_courses(self):
        # When
        response = requests.get('http://localhost:5000/course?page-number=20&page-size=10', headers={"Content-Type": "application/json"})
        # Then
        self.assertEqual(200, response.status_code)

    def test_title_page_course(self):
        # When
        response = requests.get('http://localhost:5000/course?title-words=django, python', headers={"Content-Type": "application/json"})
        # Then
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
