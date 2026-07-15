from flask_login import UserMixin
from extensions import db


class User(UserMixin ,db.Model ): # table in database
    id = db.Column(db.Integer, primary_key= True)
    username= db.Column(db.String(100), unique=True, nullable = False)
    email= db.Column(db.String(100),unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(100), nullable = False )