"""
The file contains all data models for the application
"""
list_of_users = []
list_of_books = []
books_borrowed = []


class User(object):
    """
    Hold data for user
    """

    def __init__(self):
        """This method initializes the required items"""
        self.email = None
        self.username = None
        self.password = None

    def user_serializer(self):
        """Serialize the user data"""
        user_details = {
            'email': self.email,
            'username': self.username,
            'password': self.password
        }
        return user_details

    @staticmethod
    def get_user_by_email(email):
        """This method allow to filter users by their email"""
        for user in list_of_users:
            if user.email == email:
                return user

    @staticmethod
    def get_user_by_username(username):
        """This method allow filter of users by their username"""
        for user in list_of_users:
            if user.username == username:
                return user

    def save_user(self):
        """The method is used to save the user in the list"""
        list_of_users.append(self)


class Book(object):
    """
    Hold details for books
    """
    def __init__(self):
        """This method initializes book details"""
        self.book_id = None
        self.book_title = None
        self.authors = None
        self.year = None

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
        for book in list_of_books:
            if book.book_id == book_id:
                return book

    @staticmethod
    def get_all_books():
        """This method allow user to access all books"""
        return list_of_books

    def save_book(self):
        """This method allow admin to save a book"""
        list_of_books.append(self)

    def delete_book(self):
        """This method helps in deleting an existing book"""
        list_of_books.remove(self)

    @staticmethod
    def borrow_book(book_id):
        """The method allow user to borrow an existing book"""
        for book in list_of_books:
            if book.book_id == book_id:
                books_borrowed.append(book)
                list_of_books.remove(book)
