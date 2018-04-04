"""
The file contains all data models for the application
"""
list_of_users = []
list_of_books = []

books_borrowed = []


class User(object):
    """
    Hold data for user
    """
    def __init__(self):
        self.email = None
        self.username = None
        self.password = None

    def user_serializer(self):
        return {
            'email': self.email,
            'username': self.username,
            'password': self.password
        }

    @staticmethod
    def get_user_by_email(email):
        for user in list_of_users:
            if user.email == email:
                return user

    @staticmethod
    def get_user_by_username(username):
        for user in list_of_users:
            if user.username == username:
                return user

    def save_user(self):

        list_of_users.append(self)


class Book(object):
    """
    Hold details for books
    """
    def __init__(self):
        self.book_id = None
        self.book_title = None
        self.authors = None
        self.year = None

    @staticmethod
    def book_serializer(self):
        return {
            'book_id': self.book_id,
            'book_title': self.book_title,
            'authors': self.authors,
            'year': self.year
        }

    @staticmethod
    def get_book_by_id(book_id):
        for book in list_of_books:
            if book.book_id == book_id:
                return book

    @staticmethod
    def get_all_books():
        return list_of_books

    def save_book(self):
        # book_details = self.book_serializer(self)
        list_of_books.append(self)

    def delete_book(self):
        list_of_books.remove(self)

    @staticmethod
    def borrow_book(book_id):
        for book in list_of_books:
            if book.book_id == book_id:
                books_borrowed.append(book)
                list_of_books.remove(book)
