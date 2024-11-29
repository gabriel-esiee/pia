from flask import Blueprint, request
from flask_login import login_required
from controllers.user import signup_get, signup_post, login_get, login_post, logout_get, profile_get, damages_get, oauth_google_get, authorize_google_get

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return signup_get()
    elif request.method == 'POST':
        return signup_post(request.form)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return login_get()
    elif request.method == 'POST':
        return login_post(request.form)

@user_blueprint.route('/login/oauth/google')
def oauth_google():
    return oauth_google_get()

@user_blueprint.route('/login/oauth/google/authorize')
def authorize_google():
    return authorize_google_get()

@user_blueprint.route('/logout')
@login_required
def logout():
    return logout_get()

@user_blueprint.route('/user', methods=['GET'])
@login_required
def profile():
    return profile_get()

@user_blueprint.route('/user/damages', methods=['GET'])
@login_required
def damages():
    return damages_get()
