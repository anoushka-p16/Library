from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    price = db.Column(db.Integer())
    author = db.Column(db.String(80))

    def __init__(self, title, price, author):
        self.title = title
        self.price = price
        self.author = author

    # APIs are in JSON, so this method converts the object to JSON
    def json(self):
        return {"title":self.title, "price":self.price, "author":self.author}
    