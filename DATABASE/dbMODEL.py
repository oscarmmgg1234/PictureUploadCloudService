from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE/ADMIN.sqlite'

db = SQLAlchemy(app)

class API(UserMixin,db.Model):
    __tablename__ = "API"
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(50))
    imgID = db.Column(db.String(64))
    name = db.Column(db.String(50),unique=True)
    description = db.Column(db.String(50))

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))