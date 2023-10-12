"""User database model"""

from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash





class User(UserMixin, db.Model):
    """Inherits from the baseclass db.Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        """specifies how to print objects of this class"""
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        """password hashing"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """password verification"""
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        """flask user loader function"""
        return User.query.get(int(id))


class Post(db.Model):
    """Inherits from base case db.Model"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestap = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """specifies how to print objects of this class"""
        return '<Post {}>'.format(self.body)
    

