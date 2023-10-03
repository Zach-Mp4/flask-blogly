"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, Tag, PostTag, User, Post
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

# USER ROUTES

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

# POST ROUTES

@app.route("/users/<id>/posts/new")
def new_post_form(id):
    tags = Tag.query.all()
    return render_template('new_post.html', id=id, tags = tags)

@app.route("/users/<id>/posts/new", methods=['POST'])
def new_post(id):
    title = request.form['title']
    content = request.form['content']

    post = Post(title = title, content = content, user_id = id)
    tags = request.form.getlist('checkbox')
    for tag in tags:
        print('------------')
        print(tag)
        print('------------')
        curTag = Tag.query.filter(Tag.name == tag).first()
        post.posttags.append(curTag)
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<id>")
def show_post(id):
    post = Post.query.get(id)
    user = User.query.get(post.user_id)

    return render_template('post.html', post = post, user = user)

@app.route("/posts/<id>/edit")
def edit_post_form(id):
    tags = Tag.query.all()
    return render_template('edit_post.html', id = id, tags = tags)

@app.route("/posts/<id>/edit", methods=['POST'])
def edit_post(id):
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(id)

    tags = request.form.getlist('checkbox')

    post.title = title
    post.content = content 

    for tag in tags:
        print('------------')
        print(tag)
        print('------------')
        curTag = Tag.query.filter(Tag.name == tag).first()
        post.posttags.append(curTag)

    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/posts/{id}")

@app.route("/posts/<id>/delete", methods=['POST'])
def delete_post(id):
    Post.query.filter_by(id = id).delete()
    db.session.commit()

    return redirect(f"/users")

# TAGS ROUTES

@app.route('/tags/new')
def new_tag_form():
    return render_template('new_tag.html')

@app.route('/tags/new', methods = ['POST'])
def new_tag():
    name = request.form['name']
    tag = Tag(name = name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route("/tags")
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<id>')
def show_tag_details(id):
    tag = Tag.query.get(id)

    return render_template('tag-info.html', tag = tag)

@app.route('/tags/<id>/edit')
def edit_tag_form(id):
    return render_template('tag-edit.html', id = id)

@app.route('/tags/<id>/edit', methods=['POST'])
def edit_tag(id):
    tag = Tag.query.get(id)

    name = request.form['name']
    tag.name = name

    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{id}')

@app.route('/tags/<id>/delete', methods=['POST'])
def delete_tag(id):
    Tag.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect(f'/tags')











