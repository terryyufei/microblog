from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():    
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logging Users in"""
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Create an instance for the login form
    form = LoginForm()

    # check if the form has been submitted is valid
    if form.validate_on_submit():
        # look up the user in db by their username
        user = User.query.filter_by(username=form.username.data).first()

        # Check if the user doesn't exist or if password is incorrect
        if user is None or not user.check_password(form.password.data):
            flash("Inavlid username or passowrd")
            return redirect(url_for('login'))
        
        # Login the user and remember their choice to stay logged in
        login_user(user, remember=form.remember_me.data)

        # Check if there's a next parameter in the URL & redirect to that page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    # Render the login form template when visited
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Loggig Users out"""
    logout_user()
    return redirect(url_for('index'))
