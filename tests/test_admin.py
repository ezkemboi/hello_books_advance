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
            'publisher': 'Longhorn Publishers',
            'year': 2006,
            'isnb': 23-1223322-233
        }

    # Helpers goes here
    def add_book(self, book_title: 'The Wonder Boy', authors: ['john doe', 'doe Jacob'],
                 publisher: 'Longhorn Publisher', year: 2006, isnb: 23-1223322-233):
        add_book_data = {
            'book_title': book_title,
            'authors': authors,
            'publisher': publisher,
            'year': year,
            'isnb': isnb
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

    def test_edit_book(self):
        """
        Tests for admin ability to edit book
        :return: edit_book
        """
        # add a book first by making a POST request
        rv = self.client().post(
            '/admin/api/v1/add_book',
            data={
                'book_title': 'The Beautiful Girl',
                'authors': ['Kimani John'],
                'publisher': 'The Kenya Publishers',
                'year': 2015,
                'isnb': 1233-13332-223
            }
        )
        self.assertEqual(rv.status_code, 201)

        # receive the json add book data
        results = json.loads(rv.data.decode())
        # Try editing the added book by making the put request
        rv = self.client().put(
            '/admin/api/v1/edit_book/<int:bookId>'.format(results['id']),
            data={
                'book_title': 'The Beautiful Girl 1',
                'authors': ['Kimani John', 'Jack Nick'],
                'publisher': 'The Kenya Publishers',
                'year': 2016,
                'isnb': 1234 - 13332 - 223
            }
        )
        self.assertEqual(rv.status_code, 200)

        # get edited book
        results = self.client().get(
            '/admin/api/v1/edit_book/<int:bookId>'.format(results['id'])
        )
        self.assertIn('The Beautiful Girl 1', str(results.data))

    def test_delete_book(self):
        """
        Tests the delete of existing book using DELETE request.
        :return: delete_book
        """
        rv = self.client().post(
            '/admin/api/v1/add_book',
            data={
                'book_title': 'The Beautiful Girl',
                'authors': ['Kimani John'],
                'publisher': 'The Kenya Publishers',
                'year': 2015,
                'isnb': 1233 - 13332 - 223
            }
        )
        self.assertEqual(rv.status_code, 201)
        # Get json book in json
        results = json.loads(rv.data.decode())  # decodes the stored data using loads.

        # Try delete book
        res = self.client().delete(
            '/admin/api/v1/delete_book/<int:bookId>'.format(results['id']),
        )
        self.assertEqual(res.status_code, 200)

        # test that it has been deleted, 404 error
        result = self.client().get(
            '/admin/api/v1/delete_book/1',
        )
        self.assertEqual(result.status_code, 404)


if __name__ == '__main__':
    unittest.main()













