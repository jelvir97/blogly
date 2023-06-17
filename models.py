"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
        return f"<User first_name = {self.firstName} last_name={self.last_name}>"
    
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
    