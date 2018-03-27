class User(object):
    """
    Hold data structures for user
    """
    def __init__(self, email=None, username=None, password=None):
        self.email = email
        self.username = username
        self.password = password


class Book(object):
    """
    Hold details of books
    """
    def __init__(self, book_title=None, authors=None, publisher=None, year=None, isnb=None):
        self.book_title = book_title
        self.authors = authors
        self.publisher = publisher
        self.year = year
        self.isnb = isnb

