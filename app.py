from flask import Flask, request
from flask_restful import Api, Resource
from models import db, BookModel

app = Flask(__name__)
api = Api (app) # Indicates that this is a REST API web app

# Gives SQLite information to SQLAlchemy and links DB instance from models.py with this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # Links DB with Flask app

# Resource classes
class BooksList(Resource):
    # Gets the books in DB using BookModel.query.all()
    # and displays them in JSON format
    def get(self):
        books = BookModel.query.all()
        return {'Books':list(x.json() for x in books)}
    # Converts the JSON data using request.get_json()
    # Creates and adds the new book to DB
    def post(self):
        data = request.get_json()
        new_book = BookModel(data['title'], data['price'], data['author'])
        db.session.add(new_book)
        db.session.commit()
        return new_book.json(), 201

class Book(Resource):
    # Returns the first book with the given title from the DB, or None
    # Returns the JSON of the book if found, or a 404 error if not found
    def get(self, title):
        book = BookModel.query.filter_by(title=title).first()
        if book:
            return book.json()
        return {'message': 'Book not found!'}, 404
    # Converts the JSON data using request.get_json()
    # Searches for the book with the title, replacing data or creating object
    # Adds book to the DB
    def put(self, title):
        data = request.get_json()
        book = BookModel.query.filter_by(title=title).first()
        if book:
            book.price = data['price']
            book.author = data['author']
        else:
            book = BookModel(title=title, **data)
        db.session.add(book)
        db.session.commit()
        return book.json(), 201
    # Gets the book with the title from the DB and deletes it
    def delete(self, title):
        book = BookModel.query.filter_by(title=title).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted!'}
        else:
            return {'message': 'Book not found!'}, 404

# URL endpoint for BooksList Resource
api.add_resource(BooksList, '/books')
# URL endpoint for Book Resource
api.add_resource(Book,'/book/<string:title>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=5000)
