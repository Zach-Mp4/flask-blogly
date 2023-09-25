from flask_sqlalchemy import SQLAlchemy

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