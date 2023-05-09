# from datetime import datetime
from application import db
from passlib.apps import custom_app_context as pwd_context




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(80), nullable=False)
    confirmed = False

    def hash_password(self, password):
        self.hashed_password = pwd_context.encrypt(password)
    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f'<User {self.name}>'

