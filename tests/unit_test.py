import unittest
import requests
from fastapi.testclient import TestClient
from your_fastapi_app import app  # Replace 'your_fastapi_app' with the name of your FastAPI application file

class TestCreateUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.url = 'http://127.0.0.1:8000/create-user'
        self.headers = {'Content-Type': 'application/json'}
        self.payload = {
            "user_name": "Hans Parson",
            "email": "hansparson014@gmail.com",
            "password": "123qweasd",
            "confirmation_password": "123qweasd"
        }

    def test_create_user(self):
        response = self.client.post(self.url, headers=self.headers, json=self.payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['response_code'], 'SUCCESS')
        self.assertEqual(data['response_title'], '')
        self.assertEqual(data['response_description'], '')
        self.assertEqual(data['data'], {})

class TestSignInAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.url = 'http://127.0.0.1:8000/sign-in'
        self.headers = {'Content-Type': 'application/json'}
        self.payload = {
            "email": "hansparson014@gmail.com",
            "password": "123qweasd"
        }

    def test_sign_in(self):
        response = self.client.post(self.url, headers=self.headers, json=self.payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['response_code'], 'LOGIN_SUCCESS')
        self.assertEqual(data['response_title'], 'Login Success')
        self.assertEqual(data['response_description'], '')
        self.assertIn('token', data['data'])


if __name__ == '__main__':
    unittest.main()