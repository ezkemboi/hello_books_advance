import datetime
from flask_restful import Resource
import random

from .user import token_required
from .models import Book, Borrow
from .parsers import get_parser


class BorrowBook(Resource):
    """
    This class hold function for user can borrow, return book and check history
    """
    method_decorators = [token_required]

    def post(self, current_user, book_id):
        """Post method for user to borrow book"""
        available_book = Book.query.filter_by(book_id=book_id).first()
        returned = False
        date_borrowed = datetime.datetime.now()
        due_date = datetime.datetime.now() + datetime.timedelta(days=14)
        if available_book:
            if available_book.copies >= 1:
                borrow_book = Borrow(borrow_id=random.randint(1111, 9999),
                                     book_id=book_id, user_id=current_user.user_id, returned=returned,
                                     date_borrowed=date_borrowed, due_date=due_date)
                Book.copies -= 1
                borrow_book.save_borrowed_book()
                result = borrow_book.borrow_serializer()
                return {"Book borrowed": result}, 200
            return {"Message": "The book with that id is not found"}, 404

    def put(self, current_user, book_id):
        """Put method to allow user return book"""
        return_book = Borrow.query.filter_by(book_id=book_id, returned=False).first()
        if return_book:
            return_book.user_id = current_user.user_id
            return_book.returned = True
            return_book.return_time = datetime.datetime.now()
            Book.copies += 1
            return_book.return_borrowed_book()
            return {"Message": "You have returned the book successfully."}, 200
        return {"Message": "Your trying to return unidentified book"}, 400


class BorrowHistory(Resource):
    """
    This class contains the book borrowing history
    """
    method_decorators = [token_required]

    def get(self, current_user):
        """It returns the users borrowing history"""
        args = get_parser.parse_args()
        page = args['page']
        limit = args['limit']
        returned = args['returned']

        if returned == 'false':
            un_returned_books = Borrow.query.filter_by(returned=False).all().paginate(
                page=page, per_page=limit)
            total_un_returned = un_returned_books.items
            num_results = un_returned_books.total
            num_pages = un_returned_books.pages
            current_page = un_returned_books.page
            has_next_page = un_returned_books.has_next
            has_prev_page = un_returned_books.has_prev
            prev_num = un_returned_books.prev_num
            next_num = un_returned_books.next_num
            if not un_returned_books:
                return {"Message": "You do not have books that are un-returned"}, 404
            results = [user_unreturn.borrow_serializer() for user_unreturn in total_un_returned]
            return {
                       "Total unreturned books": num_results,
                       "Total pages": num_pages,
                       "Current page": current_page,
                       "Unreturned books": results,
                       "Previous page": prev_num,
                       "Next page": next_num
                   }, 200
        else:
            all_borrowed_books = Borrow.query.filter_by(
                user_id=current_user.user_id).paginate(
                page=page, per_page=limit)
            all_borrowed = all_borrowed_books.items
            num_results = all_borrowed_books.total
            num_pages = all_borrowed_books.pages
            current_page = all_borrowed_books.page
            has_next_page = all_borrowed_books.has_next
            has_prev_page = all_borrowed_books.has_prev
            prev_num = all_borrowed_books.prev_num
            next_num = all_borrowed_books.next_num
            if not all_borrowed_books:
                return {"Message": "You have not borrowed any book."}, 404
            results = [user_borrows.borrow_serializer()
                       for user_borrows in all_borrowed]
            return {
                "Total results": num_results,
                "Number of pages": num_pages,
                "Current page": current_page,
                "All borrowed books": results,
                "Previous page": prev_num,
                "Next page": next_num
                   }, 200
