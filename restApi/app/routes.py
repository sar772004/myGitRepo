#render is to send python variable info to flask (jinja2) to write html content
# flash is to send a msg to the client browser
# url_for gets the url for a function, example index and login functions below.
from flask import render_template, flash, redirect, url_for
from app import app
#for login form
from app.forms import LoginForm

#for login management
from flask_login import current_user, login_user
from flask_login import logout_user

#for user db
from app.models import User

#for login restricted page viewing
from flask_login import login_required

#for login_required redirect and parsing
from flask import request
from werkzeug.urls import url_parse

#for date and time
from datetime import datetime

#for edit profile form
from app.forms import EditProfileForm

#for db actions
from app import db


#logging last seen this before_request is flask decorator to execute any code before any of the view functions
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


#decorator for pages, followed by the function called for that page
@app.route('/')
@app.route('/index/')
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
    return render_template("index.html", title='Home Page', posts=posts)


#for displaying users
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
# if there a redirect from login_required it will have next="page" , else it will have "index"
        next_page = request.args.get('next')
        #url_parse finds if the next page is on same website
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)        
        
    return render_template('login.html', title='Sign In', form=form)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))    

