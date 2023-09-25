"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'yurr'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route("/")
def main():
    return redirect("/users")

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template('users.html', users = users)

@app.route("/users/new")
def new_user_form():
    return render_template("new-user.html")

@app.route("/users/new", methods=['POST'])
def new_user_submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<id>")
def show_user(id):
    user = User.query.get(id)
    return render_template('user-info.html', user = user)

@app.route("/users/<id>/edit")
def edit_user(id):
    return render_template('edit-user.html', id = id)

@app.route("/users/<id>/edit", methods=['POST'])
def edit_user_db(id):
    user = User.query.get(id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    user.first_name = first_name if first_name else user.firstname
    user.last_name = last_name if last_name else user.last_name
    user.image_url = image_url if image_url else user.image_url

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{id}")

@app.route("/users/<id>/delete", methods=['POST'])
def delete_user_db(id):
    User.query.filter_by(id = id).delete()
    db.session.commit()

    return redirect(f"/users")



