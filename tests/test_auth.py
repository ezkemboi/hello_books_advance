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

    def test_login(self):
        self.assertEqual(True, False)

    def test_reset_password(self):
        self.assertEqual(True, False)

    def test_logout(self):
        pass


if __name__ == '__main__':
    unittest.main()
