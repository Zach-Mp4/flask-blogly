from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

"""Models for Blogly."""
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    last_name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    image_url = db.Column(db.String(),
                     nullable=True,
                     unique=False)
    
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    content = db.Column(db.String(),
                     nullable=False,
                     unique=False)
    created_at = db.Column(db.DateTime(),
                     nullable=False,
                     unique=False,
                     default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        unique=False)