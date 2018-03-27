import unittest

import app

import run

"""
for users; can view all books, single book
normal: {use get request}
boundaries: {}
edge: {}
unexpected: {PUT request, POST request}
"""


class HomeTestCase(unittest.TestCase):
    """
    Tests for users can view all books or a single book
    """
    def setUp(self):
        self.app = create_app(config_name="testing")
        # initialize the client
        self.client = run.app.test_client()
        # json data for predefined data
        self.book_data = {
            ""
        }

    def test_get_all_books(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
