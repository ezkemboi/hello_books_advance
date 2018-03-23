import unittest
import json

# Local imports
from app import create_app

"""
Admin can add, update and delete a book.
The book information is book title, authors, publisher, year and ISNB
normal: {book_title -> string, authors -> list containing string, publisher -> string, year -> date ISNB -> number}
boundaries: {book_title -> ["", "  ", 94, #%]: authors -> ["", "  ", 94, #%]: publisher -> ["", "  ", 94, #%]
            ISNB -> [["", "  ", #%, "akk"]}
edge: {book_title -> "too long", }
unexpected: {file, }

"""


class AdminTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        # Init the test client
        self.client = self.app.test_client
        # Json data for the predefined parameters
        self.add_book_data = {
            'book_title': 'The Wonder Boy',
            'authors': ['john doe', 'doe Jacob'],  # make sure authors is a list
            'publisher': 'Longhorn',
            'year': 2006,
            'isnb': 23-1223322-233
        }

    # Helpers goes here
    def add_book(self, book_title: 'The Wonder Boy', authors: ['john doe', 'doe Jacob'],
                 publisher: 'Longhorn', year: 2006, isnb: 23-1223322-233):
        add_book_data = {
            'book_title': book_title,
            'authors': authors,
            'publisher': publisher,
            'year': year,
            'ISNB': isnb
        }
        return self.client().post('/admin/api/v1/add_book', data=add_book_data)

    def test_add_book(self):
        """
        Test that admin should add book
        :return: add_book_data
        """
        res = self.client().post('/admin/api/v1/add_book', data=self.add_book_data)
        # Getting the results
        result = json.loads(res.data.decode())
        # make an assert of the success addition of books
        self.assertEqual(result['message'], "Admin added book successfully.")
        self.assertEqual(res.status_code, 201)


if __name__ == '__main__':
    unittest.main()













