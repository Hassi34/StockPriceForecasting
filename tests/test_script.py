import unittest, app
import os


class TestToPerform(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_page(self):
        response = self.app.get('http://localhost:8501/', follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)


