import unittest

# Local imports
from app.admin.views import Admin

"""


"""


class AdminTestCase(unittest.TestCase):
    def test_empty_title(self):
        app = Admin()
        result = app.add_title()
        self.assertEqual(result, "Title should not be empty")


if __name__ == '__main__':
    unittest.main()
