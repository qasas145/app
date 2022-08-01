from flask_sqlalchemy import SQLAlchemy
from .app import app






db = SQLAlchemy(app)

class User(db.Model) :
    id =db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
    title = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String())


    def __repr__(self) :
        return self.name
