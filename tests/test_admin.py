import unittest

# Local imports
from app.admin.views import Admin

"""
Admin can add, update and delete a book.
The book information is book title, authors, publisher, year and ISNB
normal: {book_title -> string, authors -> string, publisher -> string ISNB -> number}
boundaries: {book_title -> ["", "  ", 94, #%]: authors -> ["", "  ", 94, #%]: publisher -> ["", "  ", 94, #%]
            ISNB -> [["", "  ", #%, "akk"]}
edge: {book_title -> "too long", }
unexpected: {dict, list, file, }

"""


class AdminTestCase(unittest.TestCase):
    def test_empty_title(self):
        app = Admin()
        result = app.add_title()
        self.assertEqual(result, "Title should not be empty")


if __name__ == '__main__':
    unittest.main()
