# global imports
from flask import Flask, session, request, render_template
from flask_restful import Resource, Api
import random
import re

# Local imports
from app.models import User, Book

app = Flask(__name__)
api = Api(app)
app.secret_key = 'mysecretkeyishere'

@app.route('/')
def index():
    return render_template('docs.html')


class UserRegistration(Resource):
    def post(self):
        email = request.json.get('email')

        username = request.json.get('username')

        password = request.json.get('password')

        user = User.get_user_by_email(email)

        if not user:
            # Use re to check valid email input.
            if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip()):
                return {"Message": "Please provide a valid email."}

            # username and password contains numbers, special char or alpha. Min of 4 and 8 respectively.
            elif re.match("[A-Za-z0-9@#$%^&+=]{4,}", username.strip()) and \
                    re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password.strip()):
                create_user = User()
                create_user.email = email
                create_user.password = password
                create_user.save_user()
                return {"Message": "The User is successfully Registered."}, 201
            else:
                return {"Message": "Username and password should be min of 4 and 8 respectively."}
        else:
            return {"Message": "The user is already registered."}, 202


class UserLogin(Resource):
    def post(self):

        email = request.json.get('email')
        password = request.json.get('password')

        log_in_user = User.get_user_by_email(email)

        if log_in_user and password == log_in_user.password:
            # Call functionality to login the specified user in users list
            session['logged_in'] = True
            return {'Message': "Successfully logged in."}, 200
        else:
            return {"Message": "Wrong email or Password"}, 401


class UserLogout(Resource):
    def post(self):
        # with help of flask_login module, call logout function
        session['logged_in'] = False
        return {"Message": "Your logged out."}, 200


class ResetPassword(Resource):
    def post(self):
        # Fill the email
        email = request.json.get('email')

        # check if the email exist
        reset_user = User.get_user_by_email(email)

        if reset_user:
            password = request.json.get('password')
            if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password.strip()):
                update_email = User()
                update_email.email = email
                update_email.password = password
                update_email.save_user()
                return {"Message": "Reset Password Successful."}, 200
            else:
                return {"Message": "Password should be greater than 8"}, 400
        # return message to show un-existing email
        return {"Message": "The email does not exist."}, 404


class AddBook(Resource):
    """
    Contains all the methods to add book, list all books
    """

    # Method to add a book
    def post(self):

        book_id = random.randint(1111, 9999)  # Generate four random numbers for book_id
        book_title = request.json.get('book_title')
        authors = request.json.get('authors')
        publisher = request.json.get('publisher')
        year = request.json.get('year')
        isnb = request.json.get('isnb')

        existing_id = Book.get_book_by_id(book_id)
        existing_book = Book.get_book_by_isnb(isnb)

        if not existing_book and not existing_id:
            new_book = Book()
            new_book.book_id = book_id
            new_book.book_title = book_title
            new_book.authors = authors
            new_book.publisher = publisher
            new_book.year = year
            new_book.isnb = isnb
            new_book.save_book()
            return {"Message": "Added the book Successfully."}, 201
        return {"Message": "Fill all the details correctly."}, 400

    # method to get all books
    def get(self):
        available_books = Book.get_all_books()
        if available_books is not None:
            if len(available_books) >= 1:
                return {available_books}, 200
            else:
                return {"Message": "There is no books found"}, 404
        else:
            return {"Message": "Books not found."}


class SingleBook(Resource):

    """
    Contains all activities of a single book, including editing, getting and removing a book.
    """

    # method to update book details
    # @admin.route
    def put(self, book_id, isnb):

        # Get books by isnb and book_id
        get_book = Book.get_book_by_id(book_id)
        get_isnb = Book.get_book_by_isnb(isnb)

        # Fetch data
        book_id = get_book  # Book Id is not editable
        book_title = request.json.get('book_title')
        authors = request.json.get('authors')
        publisher = request.json.get('publisher')
        year = request.json.get('year')
        isnb = get_isnb  # ISNB of a book cannot be edited.

        if get_book:
            edited_book = Book()
            edited_book.book_id = book_id
            edited_book.book_title = book_title
            edited_book.authors = authors
            edited_book.publisher = publisher
            edited_book.year = year
            edited_book.isnb = isnb
            edited_book.save_book()
            return {"Success": "Book Updated."}, 200
        else:
            return {"Message": "The book is not found."}, 404

    # Removes a book
    # @admin.route
    def delete(self, book_id):
        get_book_id = Book.get_book_by_id(book_id)

        if get_book_id:
            get_book_id.delete()
            return {"Message": "Book deleted successfully."}, 200
        # else:
        #     print("hi")
        #     # return {"error": "Book not found."}, 204

    # method to get a single book
    def get(self, book_id):
        get_book = Book.get_book_by_id(book_id)
        if get_book:
            return {get_book}, 200
        return {"Error": "Book not found."}, 404


class Users(Resource):

    # method to allow users borrow a book.
    def post(self, book_id):

        get_book = Book.get_book_by_id(book_id)
        if get_book:
            Book.borrow_book(book_id)  # This method will append book to borrowed book and remove from available
            return {"Message": "successfully borrowed a book"}, 202
        else:
            return {"Error": "Book not found."}, 404


api.add_resource(UserRegistration, '/api/v1/auth/register')
api.add_resource(UserLogin, '/api/v1/auth/login')
api.add_resource(UserLogout, '/api/v1/auth/logout')
api.add_resource(ResetPassword, '/api/v1/auth/reset-password')

api.add_resource(AddBook, '/api/v1/books')
api.add_resource(SingleBook, '/api/v1/books/<int:book_id>')
api.add_resource(Users, '/api/v1/users/books/<book_id>')










