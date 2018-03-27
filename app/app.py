# global imports
from flask import Flask, session
from flask import request, jsonify, Blueprint
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
app.secret_key = 'mysecretkeyishere'

auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
home = Blueprint('home', __name__)


books = []
borrowed_books = []


users = []  # list that all users and their details
user_details = {}  # dict that contain key and value of each entry


class UserRegistration(Resource):
    @auth.route
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
    @auth.route
    def post(self):

        email = request.json.get('email')
        password = request.json.get('password')

        if email is None and password is None:
            return jsonify({'message': "Please enter email and password."})
        elif email == user_details['email']:
            if password == user_details['password']:
                # Call functionality to login the specified user in users list
                session['logged_in'] = True
                return jsonify({'message': "Successfully logged in."})
            return jsonify({'message': "Wrong Password"})
        return jsonify({'message': "Invalid email"})


class UserLogout(Resource):
    @auth.route
    def post(self):
        # with help of flask_login module, call logout function
        session['logged_in'] = False
        return jsonify({'message': "You have successfully logged out."})


class ResetPassword(Resource):
    @auth.route
    def post(self):
        # Fill the email
        email = request.json.get('email')

        # check if the email exist
        for user in users:
            if email == user['email']:
                password = request.json.get('password')
                if len(password) < 8:
                    return jsonify({'message': "Password should be greater than 8"})
                else:
                    user['email'] = email
                    user['password'] = password
                    users.append(user_details)
                    return jsonify({'message': "Password Reset successfully."})
            # return message to show un-existing email
        return jsonify({'message': 'The email does not exist.'})


class Book(Resource):
    """
    Contains all the methods to add book, list all books
    """

    # Method to add a book
    @admin.route
    def post(self):

        book_title = request.json.get('book_title')
        authors = request.json.get('authors')
        publisher = request.json.get('publisher')
        year = request.json.get('year')
        isnb = request.json.get('isnb')
        if book_title is not None and authors is not None and publisher is not None and year is not None and \
                        isnb is not None:
            book_details = {}
            book_details['book_id'] = len(books) + 1
            book_details['book_title'] = book_title
            book_details['authors'] = authors
            book_details['publisher'] = publisher
            book_details['year'] = year
            book_details['isnb'] = isnb
            books.append(book_details)
            return jsonify(books)
        return jsonify({'message': "Fill all the details correctly."})

    # method to get all books
    @home.route
    def get(self):
        return jsonify(books)


class SingleBook(Resource):

    """
    Contains all activities of a single book, including editing, getting and removing a book.
    """

    # method to update book details
    @admin.route
    def put(self, book_id):
        book_index = 0
        book_title = request.json.get('book_title')
        authors = request.json.get('authors')
        publisher = request.json.get('publisher')
        year = request.json.get('year')
        isnb = request.json.get('isnb')
        for book in books:
            if book_id == book['book_id']:
                book['book_title'] = book_title
                book['authors'] = authors
                book['publisher'] = publisher
                book['year'] = year
                book['isnb'] = isnb
                books[book_index] = book
                return jsonify({"Success": "Book Updated.", "Books": books})
            book_index += 1
        return jsonify({"message": "The book is not found."})

    # Removes a book
    @admin.route
    def delete(self, book_id):
        for book in books:
            if book_id == book['book_id']:
                books.remove(book)
                return jsonify({"status": "success", "message": "book deleted successfully"})
        return jsonify({"error": "book not found"})

    # method to get a single book
    @home.route
    def get(self, book_id):
        for book in books:
            if book_id == book['book_id']:
                return jsonify(book)
        return jsonify({"Error": "Book not found."})


class Users(Resource):

    # method to allow users borrow a book.
    @auth.route
    def post(self, book_id):

        for book in books:
            if book_id == book['book_id']:
                books.remove(book)
                borrowed_books.append(book)
                return jsonify({book})

        return jsonify({"Error": "Book not found."})














