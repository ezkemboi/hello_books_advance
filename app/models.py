"""
The file contains all data models for the application
"""
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    """
    Hold data for user
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, user_id, email, username, password):
        """This method initializes the required items"""
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User_id {}>".format(self.user_id)

    def user_serializer(self):
        """Serialize the user data"""
        user_details = {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'password': self.password
        }
        return user_details

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_user_by_email(email):
        """This method allow to filter users by their email"""
        return User.query.filter_by(email=email).first

    @staticmethod
    def get_user_by_username(username):
        """This method allow filter of users by their username"""
        return User.query.filter_by(username=username).first

    def save_user(self):
        """The method is used to save the user in the list"""
        db.session.add(self)
        db.session.commit()


class Book(db.Model):
    """
    Hold details for books
    """

    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String)
    authors = db.Column(db.String)
    year = db.Column(db.String)

    def __init__(self, book_id, book_title, authors, year):
        """This method initializes book details"""
        self.book_id = book_id
        self.book_title = book_title
        self.authors = authors
        self.year = year

    def __repr__(self):
        return "<Book_id {}>".format(self.book_id)

    def book_serializer(self):
        """This is a serialized book details stored in dict"""
        book_details = {
            'book_id': self.book_id,
            'book_title': self.book_title,
            'authors': self.authors,
            'year': self.year
        }
        return book_details

    @staticmethod
    def get_book_by_id(book_id):
        """This method allow user to get single book using book_id"""
        return Book.query.get(book_id)

    @staticmethod
    def get_all_books():
        """This method allow user to access all books"""
        return Book.query.all()

    def save_book(self):
        """This method allow admin to save a book"""
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        """This method helps in deleting an existing book"""
        db.session.delete(self)
        db.session.commit()


class Borrow(db.Model):
    """Class holding the models for borrow and history"""
    __tablename__ = 'borrows'

    borrow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    def __init__(self, borrow_id, user_id, book_id):
        self.borrow_id = borrow_id
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return "<Borrow_id {}>".format(self.borrow_id)

    def save_borrowed_book(self):
        db.session.add(self)
        db.session.commit()

    def return_borrowed_book(self):
        db.session.delete(self)
        db.commit()

    @staticmethod
    def borrow_book(book_id):
        """The method allow user to borrow an existing book"""
        return Borrow.query.get(book_id)


class UserBorrowHistory(db.Model):
    """Holds the history of the past books borrowed by user"""

    __tablename__ = 'histories'

    borrow_id = db.Column(db.Integer, db.ForeignKey('borrows.borrow_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    def __init__(self, borrow_id, book_id):
        self.borrow_id = borrow_id
        self.book_id = book_id

    def __repr__(self):
        return "<Borrow_id {}>".format(self.borrow_id)

    def save_borrow_history(self):
        db.session.save(self)
        db.session.commit()

    @staticmethod
    def get_borrow_history():
        return UserBorrowHistory.query.all()
