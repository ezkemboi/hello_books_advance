"""
The file contains the for user functions including register, login, logout, reset-password and logout
"""
import unittest
import json
from app import app


import run


class AuthTestCase(unittest.TestCase):
    """
    Auth test cases for register, login, logout and reset-password
    """
    def setUp(self):
        """
        Initialize the application for testing
        """
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
        self.empty_login_data = {
            'email': "",
            'password': ""
        }
        self.wrong_password_data = {
            'email': "registered@example.com",
            'password': "wrongpassword"
        }
        self.empty_register_data = {
            'email': "",
            'username': "",
            'password': ""
        }

    def register(self):
        """
        This method registers a user
        """
        return self.client.post('/api/v1/auth/register', data=json.dumps(self.user_data),
                                content_type='application/json')

    def login(self):
        """
            This method login a user
        """
        return self.client.post('/api/v1/auth/login', data=json.dumps(self.login_data),
                                content_type='application/json')

    def login_non_user(self):
        """
        This method tries to login a non-registered user
        """
        return self.client.post('/api/v1/auth/login', data=json.dumps(self.not_user), content_type='application/json')

    def register_already_registered(self):
        """
        This method register already existing user
        """
        return self.client.post('/api/v1/auth/register', data=json.dumps(self.registered_data),
                                content_type='application/json')

    def try_register_again(self):
        """
        The method registers an already registered user
        """
        return self.client.post('/api/v1/auth/register', data=json.dumps(self.already_registered),
                                content_type='application/json')

    def test_registration(self):
        """
        Test user registration
        """
        register_user = self.register()
        self.assertEqual(register_user.status_code, 201)
        result = json.loads(register_user.data.decode())
        self.assertEqual(result['Message'], 'The User is successfully Registered.')

    def test_already_registered(self):
        """
        This test code helps to eliminate double registration
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
        """
        login_res = self.login()
        result = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)
        self.assertEqual(result['Message'], "Successfully logged in.")

    def test_login_for_non_user(self):
        """
        Test non registered users cannot login
        """
        res = self.login_non_user()
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 403)
        self.assertEqual(result["Message"], "Invalid email!")

    def test_reset_password(self):
        """"
        Test reset-password
        """
        res = self.client.post('/api/v1/auth/reset-password', data=json.dumps(self.user_data),
                               content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result["Message"], "Password is reset successfully.")

    def test_logout(self):
        """
        Test for logout already logged in
        """
        login_res = self.login()
        self.assertEqual(login_res.status_code, 200)
        logout_user = self.client.post('/api/v1/auth/logout', data=json.dumps(self.login_data),
                                       content_type='application/json')
        self.assertEqual(logout_user.status_code, 200)

    def test_short_password(self):
        """
        Test for short password
        """
        register_user = self.client.post('/api/v1/auth/register', data=json.dumps(self.short_pswd),
                                         content_type='application/json')
        self.assertEqual(register_user.status_code, 400)
        res = json.loads(register_user.data.decode())
        self.assertEqual(res["Message"], "Password is short!")

    def test_empty_login_details(self):
        """
        Tests if user have not insert login details
        """
        empty_login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.empty_login_data),
                                            content_type='application/json')
        self.assertEqual(empty_login_data.status_code, 400)
        res = json.loads(empty_login_data.data.decode())
        self.assertEqual(res["Message"], "Fill all fields!")

    def test_empty_register_details(self):
        """
        Tests if user have not insert register details
        """
        empty_register_data = self.client.post('/api/v1/auth/register', data=json.dumps(self.empty_register_data),
                                               content_type='application/json')
        self.assertEqual(empty_register_data.status_code, 400)
        res = json.loads(empty_register_data.data.decode())
        self.assertEqual(res["Message"], "Provide email, username and password!")

    def test_wrong_password(self):
        """
        Test if user has provided wrong password
        """
        wrong_password = self.client.post('/api/v1/auth/login', data=json.dumps(self.wrong_password_data),
                                          content_type='application/json')
        self.assertEqual(wrong_password.status_code, 401)
        res = json.loads(wrong_password.data.decode())
        self.assertEqual(res["Message"], "Wrong password!")

if __name__ == '__main__':
    unittest.main()
