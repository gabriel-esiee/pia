from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_babel import gettext

from extensions import google, github

from services.user import MissingFields, EmailAlreadyUsed, EmailNotFound, PasswordIncorrect
from services.user import create_user, login_user, logout_user, oauth_user

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('user/signup.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        try:
            create_user(name, email, password)
        except MissingFields:
            flash('Please provide a name, email and password to create an account.', 'error')
            return redirect(url_for('main.user.signup'))
        except EmailAlreadyUsed:
            flash('The email address you provide is already associated with an account.', 'error')
            return redirect(url_for('main.user.signup'))
        else:
            flash('Your account has been created successfully. Please log in using your login details.', 'success')
            return redirect(url_for('main.user.login'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        try:
            login_user(email, password, remember)
        except MissingFields:
            flash('Please provide an email and a password to login.', 'error')
            return redirect(url_for('main.user.login'))
        except EmailNotFound:
            flash('Please check your email and try again.', 'error')
            return redirect(url_for('main.user.login'))
        except PasswordIncorrect:
            flash('Please check your password and try again.', 'error')
            return redirect(url_for('main.user.login'))
        else:
            return redirect(url_for('main.user.profile'))

@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.user.login'))

@user_blueprint.route('/user', methods=['GET'])
@login_required
def profile():
    return render_template('user/profile.html')

@user_blueprint.route('/user/damages', methods=['GET'])
@login_required
def damages():
    title = gettext("All damages")
    return render_template('damage/list.html', title=title, damages=current_user.insured_damages)

# Google OAuth.

@user_blueprint.route('/login/oauth/google')
def oauth_google():
    redirect_uri = url_for('main.user.authorize_google', _external=True, _scheme='https')
    return google.authorize_redirect(redirect_uri)

@user_blueprint.route('/login/oauth/google/authorize')
def authorize_google():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    email = user_info['email']
    name = user_info['name']
    oauth_user(name, email)
    return redirect(url_for('main.user.profile'))

# GitHub OAuth.

@user_blueprint.route('/login/oauth/github')
def oauth_github():
    redirect_uri = url_for('main.user.authorize_github', _external=True, _scheme='https')
    return github.authorize_redirect(redirect_uri)

@user_blueprint.route('/login/oauth/github/authorize')
def authorize_github():
    token = github.authorize_access_token()
    user_info = github.get('user').json()
    email_info = github.get('user/emails').json()
    name = user_info['name']
    # Get the primary email from user's email list.
    email = email_info[0]['email']
    for e in email_info:
        if e['primary']:
            email = e['email']
            break
    oauth_user(name, email)
    return redirect(url_for('main.user.profile'))
