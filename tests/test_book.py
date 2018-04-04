import unittest
import json

# Local imports
import run
from app import app

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
        self.app = app
        # Init the test client
        self.client = run.app.test_client()
        # Json data for the predefined parameters
        self.add_book_data = {
            'book_id': 1,
            'book_title': 'The Wonder Boy',
            'authors': 'john doe',
            'year': 2006,
        }
        self.modified_book = {
            'book_id': 1,
            'book_title': 'The Beautiful Girl',
            'authors': 'Kimani John',
            'year': 2015,
        }
        self.all_books = [{
            'book_id': 1,
            'book_title': 'The Wonder Boy',
            'authors': 'john doe',
            'year': 2006,
        },
            {
                'book_id': 2,
                'book_title': 'The Wonder Joy',
                'authors': 'Jackson',
                'year': 2006,
            }
        ]

    # add_book helper
    def add_book(self):
        return self.client.post('/api/v1/books', data=json.dumps(self.add_book_data),
                                content_type='application/json')

    def test_add_book(self):
        """
        Test that admin should add book
        :return: add_book_data
        """
        add_book = self.add_book()
        self.assertEqual(add_book.status_code, 201)
        # Getting the results
        result = json.loads(add_book.data.decode())
        # make an assert of the success addition of books
        self.assertEqual(result["Message"], "The book was added successfully.")

if __name__ == '__main__':
    unittest.main()
