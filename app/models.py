from flask import session

users = []  # list that all users and their details
books = []  # It holds a list of books


class User(object):
    """
    Hold data for user
    """
    def __init__(self):
        self.email = None
        self.username = None
        self.password = None

    @staticmethod
    def get_user_by_email(email):
        for user in users:
            if user.email == email:
                return user

    def save_user(self):
        users.append(self)

    @staticmethod
    def logged_in():
        session['logged_in'] = True

    @staticmethod
    def logout():
        session['logged_in'] = False


class Book(object):
    """
    Hold details for books
    """
    def __init__(self):
        self.book_id = None
        self.book_title = None
        self.authors = None
        self.publisher = None
        self.year = None
        self.isnb = None

    @staticmethod
    def get_book_by_id(book_id):
        for book in books:
            if book.book_id == book_id:
                return book

    @staticmethod
    def get_book_by_isnb(isnb):
        for book in books:
            if book.isnb == isnb:
                return book

    @staticmethod
    def get_all_books():
        for book in books:
            return book

    def save_book(self):
        books.append(self)

