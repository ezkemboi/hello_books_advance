# global imports
from flask import Flask, session
from flask import request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
app.secret_key = 'mysecretkeyishere'


books = []
borrowed_books = []


users = []  # list that all users and their details
user_details = {}  # dict that contain key and value of each entry


class UserRegistration(Resource):
    def post(self):
        email = request.json.get('email')

        username = request.json.get('username')

        password = request.json.get('password')

        if email is not None and username is not None and password is not None:
            if len(username) <= 4:
                return {"Message": "Length of username should be more than 4"}, 400
            elif len(password) < 8:
                return {"Message": "Minimum len of password is 8"}, 400

            else:
                user_details['email'] = email
                user_details['username'] = username
                user_details['password'] = password
                users.append(user_details)
                return {"Message": "The User is successfully Registered."}, 201
        return {"Message": "Email, Username and Password is required."}, 400


class UserLogin(Resource):
    def post(self):

        email = request.json.get('email')
        password = request.json.get('password')

        if email is None and password is None:
            return {'message': "Please enter email and password."}, 400
        elif email == user_details['email']:
            if password == user_details['password']:
                # Call functionality to login the specified user in users list
                session['logged_in'] = True
                return {'message': "Successfully logged in."}, 202
            return {"message": "Wrong Password"}, 401
        return {"message": "Invalid email"}, 401


class UserLogout(Resource):
    def post(self):
        # with help of flask_login module, call logout function
        session['logged_in'] = False
        return {"message": "You have successfully logged out."}, 202


class ResetPassword(Resource):
    def post(self):
        # Fill the email
        email = request.json.get('email')

        # check if the email exist
        for user in users:
            if email == user['email']:
                password = request.json.get('password')
                if len(password) < 8:
                    return {"message": "Password should be greater than 8"}, 400
                else:
                    user['email'] = email
                    user['password'] = password
                    users.append(user_details)
                    return {"message": "Password Reset successfully."}, 201
            # return message to show un-existing email
        return {"message": "The email does not exist."}, 404


class Book(Resource):
    """
    Contains all the methods to add book, list all books
    """

    # Method to add a book
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
            return {"message": "Added the book Successfully."}, 201
        return {"message": "Fill all the details correctly."}, 400

    # method to get all books
    def get(self):
        if len(books) >= 1:
            return (books), 200
        else:
            return {"message": "There is no books found"}, 404


class SingleBook(Resource):

    """
    Contains all activities of a single book, including editing, getting and removing a book.
    """

    # method to update book details
    # @admin.route
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
                return {"Success": "Book Updated."}, 201
            book_index += 1
        return {"message": "The book is not found."}, 404

    # Removes a book
    # @admin.route
    def delete(self, book_id):
        for book in books:
            if book_id == book['book_id']:
                books.remove(book)
                return {"status": "success", "message": "book deleted successfully"}, 200
        return {"error": "book not found"}, 404

    # method to get a single book
    def get(self, book_id):
        for book in books:
            if book_id == book['book_id']:
                return (book), 200
        return {"Error": "Book not found."}, 404


class Users(Resource):

    # method to allow users borrow a book.
    def post(self, book_id):

        for book in books:
            if book_id == book['book_id']:
                books.remove(book)
                borrowed_books.append(book)
                return {"message": "successfully borrowed a book"}, 202

        return {"Error": "Book not found."}, 404

api.add_resource(UserRegistration, '/api/v1/auth/register')
api.add_resource(UserLogin, '/api/v1/auth/login')
api.add_resource(UserLogout, '/api/v1/auth/logout')
api.add_resource(ResetPassword, '/api/v1/auth/reset-password')

api.add_resource(Book, '/api/v1/books')
api.add_resource(SingleBook, '/api/v1/books/<int:book_id>')
api.add_resource(Users, '/api/v1/users/books/<book_id>')










