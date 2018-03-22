from app import db
from datetime import datetime

#for password hash
from werkzeug.security import generate_password_hash, check_password_hash

#for login management
from flask_login import UserMixin

#for login loader
from app import login

#for user avatar
from hashlib import md5



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#user db classes
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #for relation between two tables users and posts
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #for adding a about me and last seen for a user
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    #for printing the username
    def __repr__(self):
        return '<User {}>'.format(self.username)   

    #for setting the hash password 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #for checking hash password to user passwd from form
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #get the avatar image using email
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)     