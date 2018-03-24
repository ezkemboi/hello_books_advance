from flask import request, jsonify, abort

# local imports
from . import admin

books = []
book_details = {}


class Admin(object):
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


