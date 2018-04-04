import unittest
import json

import run
from app import app


class AdminTestCase(unittest.TestCase):

    def setUp(self):
        """
        This set environment and initialize application
        """
        self.app = app
        self.client = run.app.test_client()
        self.add_book_data = {
            'book_id': 1,
            'book_title': 'The Wonder Boy',
            'authors': 'john doe',
            'year': 2006,
        }
        self.all_books = [{
            'book_id': 1,
            'book_title': 'The Wonder Boy',
            'authors': 'john doe',
            'year': 2006,
        }
        ]

    def add_book(self):
        """
        The function help to add book
        """
        return self.client.post('/api/v1/books', data=json.dumps(self.add_book_data),
                                content_type='application/json')

    def test_add_book(self):
        """
        Test that admin should add book
        """
        add_book = self.add_book()
        self.assertEqual(add_book.status_code, 201)
        result = json.loads(add_book.data.decode())
        self.assertEqual(result["Message"], "The book was added successfully.")

    def test_delete_book(self):
        """
        Test to delete an existing book and get the same book
        """
        self.add_book()
        delete_book = self.client.delete('/api/v1/books/1', data=json.dumps(self.add_book_data),
                                         content_type='application/json')
        self.assertEqual(delete_book.status_code, 200)
        result = json.loads(delete_book.data.decode())
        self.assertEqual(result["Message"], "Book deleted successfully.")
        get_deleted_book = self.client.get('api/v1/books/1', data=json.dumps(self.add_book_data),
                                           content_type='application/json')
        self.assertEqual(get_deleted_book.status_code, 404)
        result = json.loads(get_deleted_book.data.decode())
        self.assertEqual(result["Error"], "Book not found.")

    def test_update_book(self):
        """
        Test user updating a book
        """
        self.add_book()
        update_book = self.client.put('/api/v1/books/1', data=json.dumps(self.add_book_data),
                                      content_type='application/json')
        self.assertEqual(update_book.status_code, 200)
        result = json.loads(update_book.data.decode())
        self.assertEqual(result["Success"], "Book Updated successfully.")

    def test_get_single_book(self):
        """
        Test if a user can get a single book.
        """
        self.add_book()
        get_single_book = self.client.get('/api/v1/books/1')
        self.assertEqual(get_single_book.status_code, 200)
        get_un_existing_book = self.client.get('/api/v1/books/23')
        self.assertEqual(get_un_existing_book.status_code, 404)
        result = json.loads(get_un_existing_book.data.decode())
        self.assertEqual(result["Error"], "Book not found.")

    def test_get_all_books(self):
        """
        Test user can get all books
        """
        get_all_books = self.client.get('/api/v1/books', data=json.dumps(self.all_books),
                                        content_type='application/json')
        self.assertEqual(get_all_books.status_code, 200)

    def test_borrow_book(self):
        """
        Test user can borrow a book
        """
        borrow_book = self.client.post('/api/v1/users/books/1')
        self.assertEqual(borrow_book.status_code, 202)
        result = json.loads(borrow_book.data.decode())
        self.assertEqual(result["Message"], "successfully borrowed a book")

    def test_borrow_unavailable_book(self):
        """
        Test a user borrowing unavailable book
        """
        res = self.client.post('/api/v1/users/books/12')
        self.assertEqual(res.status_code, 404)
        result = json.loads(res.data.decode())
        self.assertEqual(result["Message"], "The book you want to borrow is unavailable.")


if __name__ == '__main__':
    unittest.main()
