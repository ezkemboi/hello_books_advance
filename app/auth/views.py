# global imports
from flask import request, jsonify

# local imports
from . import auth

users = []  # list that all users and their details
user_details = {}  # dict that contain key and value of each entry


class Auth(object):

    @auth.route('/api/v1/auth/register', methods=['POST'])
    def register(self):
        email = request.json.get('email')

        username = request.json.get('username').strip()

        password = request.json.get('password').strip()

        if email is not None and username is not None and password is not None:
            if len(username) <= 4:
                return jsonify({"Message": "Length of username should be more than 4"})
            elif len(password) < 8:
                return jsonify({"Message": "Minimum len of password is 8"})

            else:
                user_details['email'] = email
                user_details['username'] = username
                user_details['password'] = password
                users.append(user_details)
        return jsonify({"Message": "Email, Username and Password is required."})

    @auth.route('/api/v1/auth/login', methods=['POST'])
    def login(self):
        email = request.json.get('email')
        password = request.json.get('password')

        for user in users:
            if email == user_details['email']:
                if password == user_details['password']:
                    return jsonify({'message': "Successfully logged in."})
                return jsonify({'message': "Wrong Password"})
            return jsonify({'message': "Invalid email"})
        return jsonify({'message': "Please enter email and password."})


