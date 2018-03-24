import unittest
import json

from app import create_app

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
        self.app = create_app(config_name="testing")
        # Initialize the test client
        self.client = self.app.test_client
        # Make a json user data for data registration
        self.user_data = {
            'email': 'test@example.com',
            'username': 'test12',
            'password': 'password12'
        }

    # register and login helpers goes here
    def register(self, email="test@example.com", username="test12", password="password12"):
        user_data = {
            'email': email,
            'username': username,
            'password': password
        }
        return self.client().post('/api/v1/auth/register', data=user_data)

    def login(self, email="test@example.com", password="password12"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/register', data=user_data)

    def test_registration(self):
        """
        Test user registration
        :return: registration
        """
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that request contains a success message, 201 code
        self.assertEqual(result['message'], "You are registered successfully.")
        self.assertEqual(res.status_code, 201)

    def test_already_registered(self):
        """
        This test code helps to eliminate double registration
        :return: error message
        """
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Such a user already exist.")

    def test_login_for_registered_user(self):
        """
        Test the login for user already registered.
        :return: login successful
        """
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        # return the code success for registration
        self.assertEqual(res.status_code, 201)
        # define login res
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)

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
        not_user = {
            'email': 'not_user@example.com',
            'password': 'nope'
        }
        # make a post request from login
        res = self.client().post('/api/v1/auth/login', data=not_user)
        # receive the result in json
        result = json.loads(res.data.decode())
        # assert the response and return error status code 401
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid email or password, Please try again")

    def test_reset_password(self):
        self.assertEqual(True, False)

    def test_logout(self):
        pass


if __name__ == '__main__':
    unittest.main()
