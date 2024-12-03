from flask import current_app, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from flask_babel import gettext

from extensions import google, github
from models.database import db_insert
from models.user import User

def signup_get():
    return render_template('user/signup.html')

def signup_post(form):
    email = form.get('email')
    name = form.get('name')
    password = form.get('password')

    # Checks that given informations are correct.

    if not email or not name or not password:
        current_app.logger.info('user failed to signup due to missed informations.', user.email)
        flash('Please provide a name, email and password to create an account.', 'error')
        return redirect(url_for('main.user.signup'))

    # Checks that given email is not already used by another user.

    user = User.query.filter_by(email=email).first()

    if user:
        current_app.logger.info('%s failed to signup because the email is already taken.', user.email)
        flash('The email address you provide is already associated with an account.', 'error')
        return redirect(url_for('main.user.signup'))

    # Insert new user into database.

    hash = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, name=name, password=hash)
    db_insert(new_user)

    current_app.logger.info('%s signup in successfully.', new_user.email)

    flash('Your account has been created successfully. Please log in using your login details.', 'success')
    return redirect(url_for('main.user.login'))

def login_get():
    return render_template('user/login.html')

def login_post(form):
    email = form.get('email')
    password = form.get('password')
    remember = True if form.get('remember') else False

    # Checks that the user exists and that password is correct.

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        current_app.logger.info('%s failed to log in.', user.email)
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('main.user.login'))

    # Saves user in the session.

    login_user(user, remember=remember)
    current_app.logger.info('%s logged in successfully.', user.email)

    return redirect(url_for('main.user.profile'))

def logout_get():
    # Removes user from the session.

    logout_user()
    current_app.logger.info('user logged out successfully.')

    return redirect(url_for('main.user.login'))

def profile_get():
    return render_template('user/profile.html')

def damages_get():
    return render_template('damage/list.html', title=gettext("All damages"), damages=current_user.insured_damages)

# Google OAuth.

def oauth_google_get():
    redirect_uri = url_for('main.user.authorize_google', _external=True, _scheme='https')
    return google.authorize_redirect(redirect_uri)

def authorize_google_get():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    email = user_info['email']
    name = user_info['name']

    # Checks if the user already exists.

    user = User.query.filter_by(email=email).first()

    if user:
        # If the user already exists, log in him.

        login_user(user)
        current_app.logger.info('%s logged in successfully from Google.', user.email)
    else:
        # If the user doesn't already exists, create it from Google informations.

        new_user = User(email=email, name=name)
        db_insert(new_user)
        login_user(new_user)

        current_app.logger.info('%s signup successfully from Google.', new_user.email)

    return redirect(url_for('main.user.profile'))

# GitHub OAuth.

def oauth_github_get():
    redirect_uri = url_for('main.user.authorize_github', _external=True, _scheme='https')
    return github.authorize_redirect(redirect_uri)

def authorize_github_get():
    token = github.authorize_access_token()

    # Ask for profile and emails informations.

    user_info = github.get('user').json()
    email_info = github.get('user/emails').json()
    name = user_info['name']

    # Get the primary email from user's email list.

    email = email_info[0]['email']
    for e in email_info:
        if e['primary']:
            email = e['email']
            break
    
    # Checks if the user already exists.

    user = User.query.filter_by(email=email).first()

    if user:
        # If the user already exists, log in him.

        login_user(user)
        current_app.logger.info('%s logged in successfully from GitHub.', user.email)
    else:
        # If the user doesn't already exists, create it from GitHub informations.

        new_user = User(email=email, name=name)
        db_insert(new_user)
        login_user(new_user)

        current_app.logger.info('%s signup in successfully from GitHub.', new_user.email)

    return redirect(url_for('main.user.profile'))
