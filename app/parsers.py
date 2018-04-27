from flask_restful import reqparse

# Define all parsers for all classes
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, help='Please enter the email', required=True)
login_parser.add_argument('password', type=str, help='please enter the password', required=True)

register_parser = login_parser.copy()
register_parser.add_argument('username', type=str, help='Please enter the username', required=True)
register_parser.add_argument('tel_no', type=str, help='Enter the phone number', required=True)
register_parser.add_argument('address', type=str, help='Please enter address', required=True)
register_parser.add_argument('city', type=str, help='Enter your city')
register_parser.add_argument('profession', type=str, help='Enter your profession')
register_parser.add_argument('prof_img', help='Please upload your profile picture', required=True)
register_parser.add_argument('d.0.b', help='Enter the year of birth', required=True)
register_parser.add_argument('desc', type=str, help="Can you describe a little about yourself?")

reset_password_parser = login_parser.copy()

add_book_parser = reqparse.RequestParser()
add_book_parser.add_argument('book_title', type=str, help='Please enter the book title', required=True)
add_book_parser.add_argument('authors', type=str, help='Please enter the authors name', required=True, action='append')
add_book_parser.add_argument('year', help='Please enter the year published')
add_book_parser.add_argument('copies', type=int, help='Enter no of copies')
add_book_parser.add_argument('edition', type=str, help='Please enter book edition')
add_book_parser.add_argument('publisher', type=str, help='Please enter publisher')
add_book_parser.add_argument('isnb', type=str, help='Enter book isnb', action='append')
add_book_parser.add_argument('book_cover', help='Upload the book cover')

edit_book_parser = add_book_parser.copy()

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, help="Please enter page")
get_parser.add_argument('limit', type=int, help="Please enter page limit")
get_parser.add_argument('returned', type=bool)
