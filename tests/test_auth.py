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
        self.short_pswd = {
            "email": "correct@gmai.com",
            "username": "username",
            "password": "short"
        }

    # register helpers here
    def register(self):
        return self.client.post('/api/v1/auth/register', data=json.dumps(self.user_data),
                                content_type='application/json')

    # login helpers here
    def login(self):
        return self.client.post('/api/v1/auth/login', data=json.dumps(self.login_data),
                                content_type='application/json')

    # Login for non user
    def login_non_user(self):
        return self.client.post('/api/v1/auth/login', data=json.dumps(self.not_user), content_type='application/json')

    # Ensure that user is registered
    def register_already_registered(self):
        return self.client.post('/api/v1/auth/register', data=json.dumps(self.registered_data),
                                content_type='application/json')

    # Try register a registered user
    def try_register_again(self):
        return self.client.post('/api/v1/auth/register', data=json.dumps(self.already_registered),
                                content_type='application/json')

    def test_registration(self):
        """
        Test user registration
        :return: registration success
        """
        register_user = self.register()
        self.assertEqual(register_user.status_code, 201)
        result = json.loads(register_user.data.decode())
        self.assertEqual(result['Message'], 'The User is successfully Registered.')

    def test_already_registered(self):
        """
        This test code helps to eliminate double registration
        :return: error message
        """
        res = self.register_already_registered()
        self.assertEqual(res.status_code, 201)
        second_res = self.try_register_again()
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 202)
        self.assertEqual(result['Message'], 'The user is already registered.')

    def test_login_for_registered_user(self):
        """
        Test the login for user already registered.
        :return: login successful
        """
        login_res = self.login()
        result = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)
        self.assertEqual(result['Message'], "Successfully logged in.")

    def test_login_for_non_user(self):
        """
        Test non registered users cannot login
        :return: error msg 401 (unauthorized)
        """
        res = self.login_non_user()
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 403)
        self.assertEqual(result["Message"], "Invalid email!")

    def test_reset_password(self):
        """"
        Test reset-password
        :return: success when password length is met
        """
        res = self.client.post('/api/v1/auth/reset-password', data=json.dumps(self.user_data),
                               content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result["Message"], "Password is reset successfully.")

    def test_logout(self):
        """
        Test for logout already logged in
        :return: success when in session
        """
        login_res = self.login()
        self.assertEqual(login_res.status_code, 200)
        logout_user = self.client.post('/api/v1/auth/logout', data=json.dumps(self.login_data),
                                       content_type='application/json')
        self.assertEqual(logout_user.status_code, 200)

    def test_short_password(self):
        """
        Test for short password
        :return: Error message when password length is not met.
        """
        register_user = self.client.post('/api/v1/auth/register', data=json.dumps(self.short_pswd),
                                         content_type='application/json')
        self.assertEqual(register_user.status_code, 400)
        res = json.loads(register_user.data.decode())
        self.assertEqual(res["Message"], "Password is short!")

if __name__ == '__main__':
    unittest.main()
