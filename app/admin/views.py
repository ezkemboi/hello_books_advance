from flask import request, jsonify, Blueprint
from flask_restful import Resource, Api

# local imports
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
home = Blueprint('home', __name__)


books = []
book_details = {}


class Admin(Resource):
    """
    This class contains all the function, which the admin is able to undertake;
    include: adding book, updating details of book, and deleting an exiting book
    """

    @admin.route('/api/v1/books', methods=['POST'])
    def add_book(self):
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

    @auth.route('/api/v1/books/<int:bookId>', methods=['DELETE'])
    def remove_book(self, bookId):
        for book in books:
            book.delete()
            return jsonify({'Deleted': bookId})


class Books(Resource):
    """
    This class contain list of all books.
    User can get all books or one book
    access is through home blueprint, as admin, user and guest can access.
    """
    @home.route('/api/v1/books', methods=['GET'])
    def get_books(self):
        for book in books:
            return jsonify({book})

    @home.route('/api/v1/books/<int:bookId>', methods=['GET'])
    def get_a_book(self, bookId):
        for book in books:
            return jsonify({book: bookId})


class BorrowBook(Resource):
    """
    This class contains function that authenticated users can borrow books.
    """
    @auth.route('/api/v1/users/books/<bookId>', methods=['POST'])
    def borrow_book(self, bookId):
        for book in books:
            return book
        choose_book = request.json.get(bookId)
        return jsonify({'message': "Borrowed " + str(choose_book)})




