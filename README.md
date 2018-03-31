[![Build Status](https://travis-ci.org/ezrqnkemboi/hello_books.svg?branch=master)](https://travis-ci.org/ezrqnkemboi/hello_books)[![Coverage Status](https://coveralls.io/repos/github/ezrqnkemboi/hello_books/badge.svg?branch=master)](https://coveralls.io/github/ezrqnkemboi/hello_books?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/8d4476e1c37546cc8608ac5cbc290eeb)](https://www.codacy.com/app/ezrqnkemboi/hello_books?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ezrqnkemboi/hello_books&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/b92c5e43d5de4be7085b/maintainability)](https://codeclimate.com/github/ezrqnkemboi/hello_books/maintainability)

# Hello_Books API

Hello-Books is a simple application that helps manage a library and its processes like stocking, tracking and renting books. With this application users are able to find and rent books. The application also has an admin section where the admin can do things like add books, delete books, increase the quantity of a book etc.

# Deployment
    https://hello-books-library.herokuapp.com
    
# API Endpoints
|Endpoint                  | Functionality              |HTTP method 
|--------------------------|----------------------------|-------------
|/api/books                |Add a book                  |POST        
|/api/books/*book_id*       |modify a book’s information |PUT
|/api/books/*book_id*      |Remove a book               |DELETE
|/api/books                |Retrieves all books         |GET
|/api/books/*book_id*       |Get a book                  |GET
|/api/users/books/*book_id* |Borrow a book               |POST
|/api/auth/register        |Creates a user account      |POST
|/api/auth/login           |Logs in a user              |POST
|/api/auth/logout          |Logs out a user             |POST
|/api/auth/reset-password  |Password reset              |POST

# Required Features
    Users can create an account and log in
    Users can view books.
    Only Authenticated Users can borrow and return books.
    Only admin users should be able to add, modify and delete book information 
    Users can view their profile and their borrowing history
# Installation Process and Running App
 
  clone: $ git clone https://github.com/ezrqnkemboi/hello_books.git
        
  Install virtual env: $ pip install --user pipenv
       
  Go to project directory: $ cd hello_books
       
  Install env requests: $ pipenv install requests
       
  Install dependencies: $ pip install -r requirements.txt
       
  Activate virtual env: $ pipenv shell
       
  Run app: $ python run.py
    
    
# Credits

    Ezrqn Kemboi
    Andela Kenya Project
    
    

