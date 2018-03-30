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
        self.user = {
            'email': "myemail@gmail.com",
            'username': "testuser",
            'password': "passwordtrade"
        }
        self.not_user = {
            'email': 'not_user@example.com',
            'password': 'nope'
        }

    # register and login helpers to help logout user
    def register(self):
        user_data = {
            'email': "test@example.com",
            'username': "test12",
            'password': "password12"
        }
        return self.client.post('/api/v1/auth/register', data=user_data)

    def login(self):
        user_data = {
            'email': "test@example.com",
            'password': "password12"
        }
        return self.client.post('/api/v1/auth/register', data=user_data)

    def test_registration(self):
        """
        Test user registration
        :return: registration
        """
        res = self.client.post('/register', data=json.dumps(self.user), content_type='application/json')
        # assert that request contains a success message, 201 code
        self.assertIn("You are registered successfully.", str(res.data))
        self.assertEqual(res.status_code, 201)

    def test_already_registered(self):
        """
        This test code helps to eliminate double registration
        :return: error message
        """
        res = self.client.post('/register', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/api/v1/auth/register', str(res.data))
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Such a user already exist.")

    def test_login_for_registered_user(self):
        """
        Test the login for user already registered.
        :return: login successful
        """
        res = self.client.post('/api/v1/auth/register', data=json.dumps(self.user), content_type='application/json')
        # return the code success for registration
        self.assertEqual(res.status_code, 201)
        # define login res
        login_res = self.client.post('/api/v1/auth/login', data=self.user)

        # decode the json data
        result = json.loads(login_res.data.decode())
        # returning the success message and code
        self.assertEqual(result['message'], "Successfully logged in")
        # return the result status code
        self.assertEqual(login_res.status_code, 200)

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
        self.assertEqual(result['message'], "Invalid email or password, Please try again")

    def test_reset_password(self):
        res = self.client.post('/api/v1/auth/reset-password', data=json.dumps(self.user),
                               content_type='application/json')
        # receive data in json format
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['message'], "Reset Password Successful.")

    def test_logout(self):
        # call function for register
        self.register()
        # call function to login the user
        self.login()
        # Logout the user now
        res = self.client.post('/api/v1/auth/logout')
        self.assertEqual(res.status_code, 200)
        self.assertEqual('Message', "Your logged out.")


if __name__ == '__main__':
    unittest.main()
