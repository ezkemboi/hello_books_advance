from flask import request, jsonify, abort

# local imports
from . import admin


class Admin(object):

    @admin.route('/api/v1/books', methods=['POST'])
    def add_book(self):
        return "Added a book successfully"

