# global imports
from flask import Flask
from flask_login import login_user, login_required, logout_user
from flask import request, jsonify, Blueprint
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
home = Blueprint('home', __name__)


books = []
book_details = {}


users = []  # list that all users and their details
user_details = {}  # dict that contain key and value of each entry


class UserRegistration(Resource):

    @auth.route('/api/v1/auth/register')
    def post(self):
        email = request.json.get('email')

        username = request.json.get('username')

        password = request.json.get('password')

        if email is not None and username is not None and password is not None:
            if len(username) <= 4:
                return jsonify({"Message": "Length of username should be more than 4"})
            elif len(password) < 8:
                return jsonify({"Message": "Minimum len of password is 8"})

            else:
                user_details['email'] = email
                user_details['username'] = username
                user_details['password'] = password
                users.append(user_details)
                return jsonify({"Message": "The User is successfully Registered."})
        return jsonify({"Message": "Email, Username and Password is required."})


class UserLogin(Resource):

    @auth.route('/api/v1/auth/login')
    def post(self):

        email = request.json.get('email')
        password = request.json.get('password')

        if email is None and password is None:
            return jsonify({'message': "Please enter email and password."})
        elif email == user_details['email']:
            if password == user_details['password']:
                # Call functionality to login the specified user in users list
                return jsonify({'message': "Successfully logged in."})
            return jsonify({'message': "Wrong Password"})
        return jsonify({'message': "Invalid email"})


class UserLogout(Resource):

    @auth.route('/api/v1/auth/logout')
    @login_required
    def post(self):
        # with help of flask_login module, call logout function
        logout_user()
        return jsonify({'message': "You have successfully logged out."})


class ResetPassword(Resource):

    @auth.route('/api/v1/auth/reset-password')
    def post(self):
        # Fill the email
        email = request.json.get('email')

        # check if the email exist
        if email in user_details['email']:
            password = request.json.get('password')
            if password < 8:
                return jsonify({'message': "Password should be greater than 8"})
            else:
                user_details['email'] = email
                user_details['password'] = password
                users.append(user_details)
                return jsonify({'message': "Password Reset successfully."})
        # return message to show un-existing email
        return jsonify({'message': 'The email does not exist.'})


class Book(Resource):
    """
    Contains all the methods to add book, list all books
    """

    @admin.route('/api/v1/books')
    # Method to add a book
    def post(self):
        book_title = request.json.get('book_title')
        authors = request.json.get('authors')
        publisher = request.json.get('publisher')
        year = request.json.get('year')
        isnb = request.json.get('isnb')
        if book_title is not None and authors is not None and publisher is not None and year is not None and \
                        isnb is not None:
            book_details['book_title'] = book_title
            book_details['authors'] = authors
            book_details['publisher'] = publisher
            book_details['year'] = year
            book_details['isnb'] = isnb
            books.append(book_details)
            return jsonify({'message': "Added the book successfully."})
        return jsonify({'message': "Fill all the details correctly."})

    @admin.route('/api/v1/books')
    # method to get all books
    def get(self):
        return jsonify(books)


class SingleBook(Resource):

    """
    Contains all activities of a single book, including editing, getting and borrow book.
    """

    @auth.route('/api/v1/books/<int:book_id>')
    # Removes a book
    def delete(self, book_id):
        for book in books:
            book.delete(book_id)
            return jsonify({'message': "The book is deleted."})

    @home.route('/api/v1/books/<int:book_id>', methods=['GET'])
    # method to get a single book
    def get(self, book_id):
        for book in books:
            return jsonify({book: book_id})


class Users(Resource):

    @auth.route('/api/v1/users/books/<book_id>')
    # method to allow users borrow a book.
    def post(self, book_id):
        for book in books:
            return book
        choose_book = request.json.get(book_id)
        return jsonify({'message': "Borrowed " + str(choose_book)})

    # @admin.route('/api/v1/books/<book_id>')
    # def put(self, book_id):
    #     for book in books:




