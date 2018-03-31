import unittest
import json
from app import app


import run

"""
Authenticated users can; register, login, logout, reset-password and borrow books
normal: {email -> string, username -> string, password -> string}
boundaries: {}
edge: {}
unexpected: {email -> number, character, invalid email structure: username -> "too long", numerical; password -> "too short",
"too long"}
"""


class AuthTestCase(unittest.TestCase):
    """
    Auth test cases for register, login, logout and reset-password
    """
    def setUp(self):
        self.app = app
        self.client = run.app.test_client()
        self.already_registered = {
            'email': "registered@example.com",
            'username': "registered",
            'password': "registeredpassword"
        }
        self.registered_data = {
            'email': "registered@example.com",
            'username': "registered",
            'password': "registeredpassword"
        }
        self.user_data = {
            'email': "myemail@gmail.com",
            'username': "testuser",
            'password': "passwordtrade"
        }
        self.login_data = {
            'email': "registered@example.com",
            'password': "registeredpassword"
        }
        self.not_user = {
            'email': 'not_user@example.com',
            'password': 'nope'
        }

    # register helpers here
    def register(self, user_data):
        register_user = self.client.post('/api/v1/auth/register', data=user_data)
        return register_user

    # login helpers here
    def login(self, login_data):
        login = self.client.post('/api/v1/auth/register', data=login_data)
        return login

    def test_registration(self):
        """
        Test user registration
        :return: registration
        """
        register_user = self.client.post('/api/v1/auth/register', data=json.dumps(self.user_data),
                                         content_type='application/json')
        self.assertEqual(register_user.status_code, 201)
        result = json.loads(register_user.data.decode())
        self.assertEqual(result['Message'], 'The User is successfully Registered.')

    def test_already_registered(self):
        """
        This test code helps to eliminate double registration
        :return: error message
        """
        res = self.client.post('/api/v1/auth/register', data=json.dumps(self.registered_data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/api/v1/auth/register', data=json.dumps(self.already_registered),
                                      content_type='application/json')
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 202)
        self.assertEqual(result['Message'], 'The user is already registered.')

    def test_login_for_registered_user(self):
        """
        Test the login for user already registered.
        :return: login successful
        """

        # define login res
        login_res = self.client.post('/api/v1/auth/login', data=json.dumps(self.login_data),
                                     content_type='application/json')
        # decode the json data
        result = json.loads(login_res.data.decode())
        # return the result status code
        self.assertEqual(login_res.status_code, 200)
        # returning the success message and code
        self.assertEqual(result['Message'], "Successfully logged in.")

    def test_login_for_non_user(self):
        """
        Test non registered users cannot login
        :return: error msg 401 (unauthorized)
        """
        # make a post request from login
        res = self.client.post('/api/v1/auth/login', data=json.dumps(self.not_user), content_type='application/json')
        # receive the result in json
        result = json.loads(res.data.decode())
        # assert the response and return error status code 401
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result["Message"], "Wrong email or Password")

    def test_reset_password(self):
        res = self.client.post('/api/v1/auth/reset-password', data=json.dumps(self.user_data),
                               content_type='application/json')
        # receive data in json format
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['Message'], "Reset Password Successful.")

    def test_logout(self):
        login_res = self.client.post('/api/v1/auth/login', data=json.dumps(self.login_data),
                                     content_type='application/json')
        self.assertEqual(login_res.status_code, 200)

        logout_user = self.client.post('/api/v1/auth/logout', data=json.dumps(self.login_data),
                                       content_type='application/json')
        # result = json.loads(logout_user.data)
        self.assertEqual(logout_user.status_code, 200)


if __name__ == '__main__':
    unittest.main()
