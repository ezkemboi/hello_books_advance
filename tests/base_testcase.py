import unittest

# Local imports
from app.app import app
from app.endpoints import api
from app.models import User, Book


class BaseTestCase(unittest.TestCase):
    """"
    These are the base class tests.
    """
    def setUp(self):
        self.app = app
        self.__client = self.app.test_client
        self.user = {'email': 'test@example.com', 'username': 'test12', 'password': 'mypassword'}
        self.wrong_user = {'email': 'wrong@example.com', 'username': 'wrong12', 'password': 'wrongpassword'}

        with self.app.app_context():
            user = User(email="test@example.com", username="test12", password="mypassword")



if __name__ == '__main__':
    unittest.main()
