"""Blogly application."""
from flask import Flask, request,render_template, redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
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
    return redirect('/users')

@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('user_list.html',users=users)

@app.route('/users/new')
def user_form():
    return render_template('user_form.html')