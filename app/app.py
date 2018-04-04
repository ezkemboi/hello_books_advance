"""
This file holds all the resources for user from registration to borrow books and return books
"""
from flask import Flask, session, render_template
from flask_restful import Resource, Api, reqparse
import re

from app.models import User, Book

app = Flask(__name__)
api = Api(app, prefix='/api/v1')
app.secret_key = 'mysecretkeyishere'


@app.route('/')
def index():
    """
    It holds the homepage url and renders the generated html doc for api documentation
    """
    return render_template('docs.html')

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, help='Email', required=True)
login_parser.add_argument('password', type=str, help='Password', required=True)


class UserLogin(Resource):
    """
    It holds user login functionality
    """

    def post(self):
        """
        The post method logs in user
        """
        args = login_parser.parse_args()
        email = args['email']
        password = args['password']

        if not email or not password:
            return {"Message": "Fill all fields!"}, 400

        log_in_user = User.get_user_by_email(email)

        if not log_in_user:
            return {"Message": "Invalid email!"}, 403

        elif log_in_user and password == log_in_user.password:
            session['logged_in'] = True
            return {'Message': "Successfully logged in."}, 200
        else:
            return {"Message": "Wrong password!"}, 401

register_parser = login_parser.copy()
register_parser.add_argument('username', type=str, help='Username', required=True)


class UserRegistration(Resource):
    """
        It holds user registration functionality
    """

    def post(self):
        """
        Post method for user registration
        """
        args = register_parser.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']

        user = User.get_user_by_email(email)
        valid_email = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())
        valid_username = re.match("[A-Za-z0-9@#$%^&+=]{4,}", username.strip())
        password_length = re.match("[A-Za-z0-9@#$%^&+=]{8,}", password.strip())

        if email is None or username is None or password is None:
            return {"Message": "Provide email, username and password!"}, 400

        username = User.get_user_by_username(username)

        if username:
            return {"Message": "The username is already taken!"}, 409

        if not user:
            if not valid_email:
                return {"Message": "Please provide a valid email!"}, 400
            elif not valid_username:
                return {"Message": "Username need to be more than 4 characters!"}, 400
            elif not password_length:
                return {"Message": "Password is short!"}, 400
            else:
                create_user = User()
                create_user.email = email
                create_user.password = password
                create_user.save_user()
                return {"Message": "The User is successfully Registered."}, 201
        else:
            return {"Message": "The user is already registered."}, 202


class UserLogout(Resource):
    """
        It holds user logout functionality
    """
    def post(self):
        """
        Post Method to logout user
        """
        session['logged_in'] = False
        return {"Message": "Your logged out."}, 200


reset_password_parser = login_parser.copy()


class ResetPassword(Resource):
    """
        It holds user reset password functionality
    """
    def post(self):
        """
        The method allow user to reset password
        """
        args = reset_password_parser.parse_args()
        email = args['email']

        reset_user = User.get_user_by_email(email)

        if reset_user:
            password = args['password']
            password_length = re.match("[A-Za-z0-9@#$%^&+=]{8,}", password.strip())
            if password_length:
                update_email = User()
                update_email.email = email
                update_email.password = password
                update_email.save_user()
                return {"Message": "Password is reset successfully."}, 200
            else:
                return {"Message": "Password is short!"}, 400
        return {"Message": "The email does not exist."}, 404

add_book_parser = reqparse.RequestParser()
add_book_parser.add_argument('book_id', type=int, help='Book Id', required=True)
add_book_parser.add_argument('book_title', type=str, help='Book Title', required=True)
add_book_parser.add_argument('authors', type=str, help='Authors Name', required=True)
add_book_parser.add_argument('year', type=int, help='Year Published')


class AddBook(Resource):
    """
    Contains all the methods to add book, list all books
    """

    def post(self):
        """
        Post method to allow addition of book
        """
        args = add_book_parser.parse_args()
        book_id = args['book_id']
        book_title = args['book_title']
        authors = args['authors']
        year = args['year']

        existing_id = Book.get_book_by_id(book_id)
        if existing_id:
            return {"Message": "A book with that id already exist."}, 400
        elif not existing_id:
            new_book = Book()
            new_book.book_id = book_id
            new_book.book_title = book_title
            new_book.authors = authors
            new_book.year = year
            new_book.save_book()
            return {"Message": "The book was added successfully."}, 201
        else:
            return {"Message": "You have entered wrong inputs."}, 400

    def get(self):
        """
        Get method to get all books
        """
        available_books = Book.get_all_books()
        if available_books:
            return {available_books}, 200
        else:
            return {"Message": "Books not found."}


edit_book_parser = add_book_parser.copy()
edit_book_parser.remove_argument('book_id')
delete_book_parser = reqparse.RequestParser()


class SingleBook(Resource):

    """
    Contains all activities of a single book, including editing, getting and removing a book.
    """

    def put(self, book_id):
        """
        Put method to edit already existing book
        """
        args = edit_book_parser.parse_args()
        get_book = Book.get_book_by_id(book_id)

        book_title = args['book_title']
        authors = args['authors']
        year = args['year']

        if get_book:
            edited_book = Book()
            edited_book.book_id = get_book.book_id
            edited_book.book_title = book_title
            edited_book.authors = authors
            edited_book.year = year
            edited_book.save_book()
            return {"Success": "Book Updated successfully."}, 200
        else:
            return {"Message": "The book is not found."}, 404

    def delete(self, book_id):
        """
        Delete method to delete a single book
        """

        if book_id:
            get_book_id = Book.get_book_by_id(book_id)
            if get_book_id:
                get_book_id.delete_book()
                return {"Message": "Book deleted successfully."}, 200
            return {"Error": "Book not found."}, 404

    def get(self, book_id):
        """
        Get method for a single book
        """
        if book_id:
            get_book = Book.get_book_by_id(book_id)
            if get_book:
                return {'book_id': get_book.book_id,
                        'book_title': get_book.book_title,
                        'authors': get_book.authors
                        }, 200
            return {"Error": "Book not found."}, 404


class Borrow(Resource):
    """
    This class hold function for user can borrow, return book and check history
    """

    def post(self, book_id):
        """
        Post method for user to borrow book
        """
        get_book = Book.get_book_by_id(book_id)
        if get_book:
            Book.borrow_book(book_id)
            return {"Message": "successfully borrowed a book"}, 202
        else:
            return {"Message": "The book you want to borrow is unavailable."}, 404


api.add_resource(UserRegistration, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogout, '/auth/logout')
api.add_resource(ResetPassword, '/auth/reset-password')

api.add_resource(AddBook, '/books')
api.add_resource(SingleBook, '/books/<int:book_id>')
api.add_resource(Borrow, '/users/books/<int:book_id>')
