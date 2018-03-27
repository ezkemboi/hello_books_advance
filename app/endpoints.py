from app.app import api
from app.app import UserLogin, UserLogout, UserRegistration, ResetPassword, Book, SingleBook, Users


api.add_resource(UserRegistration, '/api/v1/auth/register')
api.add_resource(UserLogin, '/api/v1/auth/login')
api.add_resource(UserLogout, '/api/v1/auth/logout')
api.add_resource(ResetPassword, '/api/v1/auth/reset-password')

api.add_resource(Book, '/api/v1/books')
api.add_resource(SingleBook, '/api/v1/books/<int:book_id>')
api.add_resource(Users, '/api/v1/users/books/<book_id>')
