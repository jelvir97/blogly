"""Blogly application."""
from flask import Flask, request,render_template, redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    """Renders form to add new post"""
    return render_template('post_form.html',user_id=user_id)

@app.route('/users/<user_id>/posts/new',methods = ['POST'])
def new_post(user_id):
    """Handles new blogpost POST request"""
    title= request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=int(user_id))
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def post_details(post_id):
    """Renders page with post title,content and date created"""
    post = Post.query.get(int(post_id))
    return render_template('post_details.html',post=post)

@app.route('/posts/<post_id>/edit')
def post_edit(post_id):
    """Renders form to edit existing post"""
    post = Post.query.get(int(post_id))
    return render_template('post_edit.html',post=post)

@app.route('/posts/<post_id>/edit',methods=['POST'])
def post_update(post_id):
    """Handles edit post POST request"""
    post= Post.query.get(int(post_id))
    resp = request.form
    post.title = resp['title'] if resp['title'] else post.title
    post.content = resp['content'] if resp['content'] else post.content
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    """Deletes Post"""
    post = Post.query.get(int(post_id))
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def tags_list():
    tags = Tag.query.all()
    return render_template('tags_list.html',tags=tags)

@app.route('/tags/new')
def tags_new_form():
    return render_template('tag_form.html')

@app.route('/tags/new', methods=["POST"])
def tags_new():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get(int(tag_id))
    return render_template('tag_details.html',tag=tag)

@app.route('/tags/<tag_id>/edit')
def tags_edit_form(tag_id):
    tag = Tag.query.get(int(tag_id))
    return render_template('tag_edit.html',tag=tag)

@app.route('/tags/<tag_id>/edit',methods=["POST"])
def tags_edit(tag_id):
    tag = Tag.query.get(int(tag_id))
    tag.name = request.form["name"]
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags')

@app.route('/tags/<tag_id>/delete')
def tags_delete(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')