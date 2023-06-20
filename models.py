"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""
id pk
first_name
last_name
img_url
"""
class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        return f"<User first_name = {self.first_name} last_name={self.last_name}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                     nullable=False)
    
    last_name = db.Column(db.String(50),
                     nullable=False)
    
    img_url = db.Column(db.String(),
                     nullable=False,
                     default='https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png')
    
    posts = db.relationship('Post')
    

class Post(db.Model):
    __tablename__ = "posts"

    def __repr__(self):
        return f"<User id = {self.id} title = {self.title} created_at={self.created_at}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(50),
                     nullable=False)
    
    content = db.Column(db.String(500),
                     nullable=False)
    
    created_at = db.Column(db.DateTime,default=datetime.now(),
                     nullable=False,)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)