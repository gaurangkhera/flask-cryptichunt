from hack import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64),index=True)
    password = db.Column(db.String)
    ans_time = db.Column(db.Integer, nullable=False, default=datetime.now)
    correct_ans = db.Column(db.Integer, default=0, nullable=False)
    queries = db.relationship('ContactQuery', backref='user')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String, nullable=False)
    ans = db.Column(db.String, nullable=False)

class ContactQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    poster = db.Column(db.String, db.ForeignKey('user.username'))


