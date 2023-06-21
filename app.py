"""Blogly application."""
from flask import Flask, request,render_template, redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from sqlalchemy import Text, text

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'woohoo!123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)

@app.route('/')
def home_page():
    """Redirects to /users"""
    return redirect('/users')

@app.route('/users')
def users_list():
    """Queries all users and lists them on a page"""
    users = User.query.all()
    return render_template('user_list.html',users=users)

@app.route('/users/new')
def user_form():
    """Renders a form to add new user to db"""
    return render_template('user_form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Handles post request for add user form. Redirects to /users"""
    first= request.form['first-name']
    last = request.form['last-name']
    img = request.form['img-url']
    img = img if img else None
    user = User(first_name=first,last_name=last,img_url=img)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def user_detail(user_id):
    """Renders page displaying user details."""
    user = User.query.get(int(user_id))
    posts = Post.query.filter(Post.user_id == int(user_id)).all()

    return render_template('user_detail.html',user=user,posts=posts)

@app.route('/users/<user_id>/edit')
def edit_user_detail(user_id):
    """Renders user edit form."""
    user = User.query.get(int(user_id))
    return render_template('edit_user_form.html',user=user)

@app.route('/users/<user_id>/edit',methods = ['POST'])
def update_user_detail(user_id):
    """Handles user edit post request. Redirects to same user's details page."""
    user = User.query.get(int(user_id))
    resp = request.form
    
    user.first_name = resp['first-name'] if resp['first-name'] else user.first_name
    user.last_name = resp['last-name'] if resp['last-name'] else user.last_name
    user.img_url = resp['img-url'] if resp['img-url'] else user.img_url

    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    """Deletes user from db"""
    user = User.query.get(int(user_id))
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>/posts/new')
def new_post_form(user_id):
    return render_template('post_form.html',user_id=user_id)

@app.route('/users/<user_id>/posts/new',methods = ['POST'])
def new_post(user_id):
    title= request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=int(user_id))
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def post_details(post_id):
    post = Post.query.get(int(post_id))
    return render_template('post_details.html',post=post)