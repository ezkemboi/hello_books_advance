"""
The file contains all data models for the application
"""
import jwt
from datetime import datetime, timedelta
from flask import current_app

from app import db


class User(db.Model):
    """
    Hold data for user
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tel_no = db.Column(db.String)
    profession = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    prof_img = db.Column(db.LargeBinary)
    DOB = db.Column(db.DateTime)
    about_you = db.Column(db.String)
    borrows = db.relationship('Borrow', backref='user', lazy='dynamic')
    plans = db.relationship('Plan', backref='user', lazy='dynamic')

    def user_serializer(self):
        """Serialize the user data"""
        user_details = {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'tel_no': self.tel_no,
            'profession': self.profession,
            'address': self.address,
            'prof_img': self.prof_img,
            'DOB': self.DOB,
            'about_you': self.about_you
        }
        return user_details

    def save_user(self):
        """The method is used to save the user in the list"""
        db.session.add(self)
        db.session.commit()

    def update_user(self):
        db.session.commit(self)

    def generate_token(self, user_id):
        """Generate token for user authentication"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the generated token via the authorization header"""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "This token is expired. Please login to get new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class Book(db.Model):
    """
    Hold details for books
    """

    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    edition = db.Column(db.String)
    publisher = db.Column(db.String)
    isnb = db.Column(db.Integer)
    book_cover = db.Column(db.LargeBinary)
    borrows = db.relationship('Borrow', backref='book', lazy='dynamic')

    def book_serializer(self):
        """This is a serialized book details stored in dict"""
        book_details = {
            'book_id': self.book_id,
            'book_title': self.book_title,
            'authors': self.authors,
            'year': self.year,
            'copies': self.copies,
            'edition': self.edition,
            'publisher': self.publisher,
            'isnb': self.isnb,
            'book_cover': self.book_cover
        }
        return book_details

    def save_book(self):
        """This method allow admin to save a book"""
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        """This method helps in deleting an existing book"""
        db.session.delete(self)
        db.session.commit()

    def update_book(self):
        """Update a book edited by the admin"""
        db.session.commit(self)


class Borrow(db.Model):
    """Class holding the models for borrow and history"""
    __tablename__ = 'borrows'

    borrow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    book_id = db.Column(db.Integer, db.ForeignKey(Book.book_id))
    date_borrowed = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    return_time = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, nullable=False)

    def borrow_serializer(self):
        """Serialize data for borrow"""
        borrow_details = {
            'borrow_id': self.borrow_id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'returned': self.returned,
            'book_title': self.book_title,
            'isnb': self.isnb
        }
        return borrow_details

    def save_borrowed_book(self):
        """Save a book borrowed by the user"""
        db.session.add(self)
        db.session.commit()

    def return_borrowed_book(self):
        db.session.commit(self)


class Plan(db.Model):
    """Plans that user subscribe to"""
    __tablename__ = 'plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    limited_monthly_3 = db.Column(db.Boolean, nullable=True, default=False)
    limited_monthly_6 = db.Column(db.Boolean, nullable=True, default=False)
    unlimited_monthly_3 = db.Column(db.Boolean, nullable=True, default=False)
    unlimited_monthly_6 = db.Column(db.Boolean, nullable=True, default=False)
    limited_yearly_3 = db.Column(db.Boolean, nullable=True, default=False)
    limited_yearly_6 = db.Column(db.Boolean, nullable=True, default=False)
    unlimited_yearly_3 = db.Column(db.Boolean, nullable=True, default=False)
    unlimited_yearly_6 = db.Column(db.Boolean, nullable=True, default=False)
    expiry = db.Column(db.DateTime)
    payment_date = db.Column(db.DateTime)
    charges = db.Column(db.Float)

    def save_plans(self):
        """Save user plans"""
        db.session.add(self)
        db.session.commit()

    def delete_plans(self):
        """Unsubscribe plans"""
        db.session.delete(self)
        db.session.commit()

    def update_plans(self):
        """Upgrade or downgrade of plans"""
        db.session.commit(self)


class BlacklistToken(db.Model):
    """
    Create a table for blacklisted tokens
    """
    __tablename__ = "blacklisted_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.column(db.String)
    blacklisted = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        """Initialize token blacklist"""
        self.token = token
        self.blacklisted = datetime.utcnow()

    def save_token(self):
        """Save blacklisted token"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklisted(token):
        blacklisted = BlacklistToken.query.filter_by(
            token=str(token)).first()
        if blacklisted:
            return True
        return False
