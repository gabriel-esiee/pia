from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from app import google
from app.models.database import insert
from app.models.user import User

def signup_get():
    return render_template('user/signup.html')

def signup_post(form):
    email = form.get('email')
    name = form.get('name')
    password = form.get('password')
    if not email or not name or not password:
        flash('Please provide a name, email and password to create an account.', 'error')
        return redirect(url_for('main.user.signup'))

    user = User.query.filter_by(email=email).first()
    if user:
        flash('The email address you provide is already associated with an account.', 'error')
        return redirect(url_for('main.user.signup'))

    hash = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, name=name, password=hash)
    insert(new_user)

    flash('Your account has been created successfully. Please log in using your login details.', 'success')
    return redirect(url_for('main.user.login'))

def login_get():
    return render_template('user/login.html')

def login_post(form):
    email = form.get('email')
    password = form.get('password')
    remember = True if form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('main.user.login'))

    login_user(user, remember=remember)
    
    return redirect(url_for('main.user.profile'))

def oauth_google_get():
    redirect_uri = url_for('main.user.authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

def authorize_google_get():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    email = user_info['email']
    name = user_info['name']

    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
    else:
        new_user = User(email=email, name=name)
        insert(new_user)
        login_user(new_user)

    # session['user'] = user_info
    return redirect(url_for('main.user.profile'))

def logout_get():
    session.pop('user', None)
    logout_user()
    return redirect(url_for('main.user.login'))

def profile_get():
    return render_template('user/profile.html')

def damages_get():
    return render_template('damage/list.html', title="All your damages", damages=current_user.insured_damages)
