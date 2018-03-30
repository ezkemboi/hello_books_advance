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
            'book_id': 7898,
            'book_title': 'The Wonder Boy',
            'authors': ['john doe', 'doe Jacob'],  # make sure authors is a list
            'publisher': 'Longhorn Publishers',
            'year': "2006",
            'isnb': "23-1223322-233"
        }
        self.modified_book = {
            'book_id': 7898,
            'book_title': 'The Beautiful Girl',
            'authors': 'Kimani John',
            'publisher': 'The Kenya Publishers',
            'year': "2015",
            'isnb': "23-1223322-233"
        }

    # Helpers goes here

    def test_add_book(self):
        """
        Test that admin should add book
        :return: add_book_data
        """
        add_book = self.client.post('/api/v1/books', data=json.dumps(self.add_book_data),
                                    content_type='application/json')
        # Getting the results
        result = json.loads(add_book.data.decode())
        # make an assert of the success addition of books
        self.assertEqual(add_book.status_code, 201)
        self.assertEqual(result['message'], 'Added the book Successfully.')

    def test_edit_book(self):
        """
        Tests for admin ability to edit book
        :return: edit_book
        """
        # add a book first by making a POST request

        add_book_result = self.client.post(
            '/api/v1/books',
            data=json.dumps(self.add_book_data),
            content_type='application/json'
        )
        self.assertEqual(add_book_result.status_code, 201)

        # Try editing the added book by making the put request
        self.modified_book['book_id'] = 7898
        self.modified_book['isnb'] = "23-1223322-233"
        book_edit = self.client.put(
            '/api/v1/books/7898',
            data=json.dumps(self.modified_book), content_type='application/json')
        result = json.loads(book_edit.data.decode())
        self.assertEqual(book_edit.status_code, 200)
        result_book = self.client.get('/api/books/7898')
        self.assertIn("23-1223322-233", str(result_book))
        self.assertEqual(result['success'], 'Book Updated.')

    def test_delete_book(self):
        """
        Tests the delete of existing book using DELETE request.
        :return: delete_book
        """
        # self.add_book_data['book_id'] = 7898
        # rv = self.client.post(
        #     '/api/v1/books',
        #     data=json.dumps(self.add_book_data), content_type='application/json')
        # self.assertEqual(rv.status_code, 201)

        # Try delete book
        res = self.client.delete(
            '/api/v1/books/7898', data=json.dumps(self.add_book_data), content_type='application/json'
        )
        # result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual('message', 'Book deleted successfully.')

        # # # test that it has been deleted, 204 error
        # result = self.client.get(
        #     '/api/v1/books/7898',
        # )
        # self.assertEqual(result.status_code, 204)
        # self.assertEqual("Error", "Book not found.")


if __name__ == '__main__':
    unittest.main()
