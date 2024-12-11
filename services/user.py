from flask import current_app
from flask_login import current_user
from flask_login import login_user as flask_login_user
from flask_login import logout_user as flask_logout_user
from werkzeug.exceptions import Unauthorized, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from models.database import db_insert, db_pop, db_commit
from models.user import User
from models.user_role import UserRole

class MissingFields(BadRequest):
    def __init__(self, message="Missing fields"):
        super().__init__(message)

class EmailAlreadyUsed(BadRequest):
    def __init__(self, message="Email address already in use"):
        super().__init__(message)

class EmailNotFound(BadRequest):
    def __init__(self, message="Email address not found"):
        super().__init__(message)

class PasswordIncorrect(BadRequest):
    def __init__(self, message="Password is incorrect"):
        super().__init__(message)

def is_user_connected() -> bool:
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    return True

def is_current_user_admin() -> bool:
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.is_admin():
        raise Unauthorized("User is not administrator")
    return True

def get_user_by_email(email:str) -> User:
    return User.query.filter_by(email=email).first()

def create_user(name:str, email:str, password:str) -> User:
    if not email or not name:
        current_app.logger.info('User failed to signup due to missed information.')
        raise MissingFields()
    if get_user_by_email(email):
        current_app.logger.info('User failed to signup because the email is already taken.')
        raise EmailAlreadyUsed()
    hash = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, name=name, password=hash)
    db_insert(new_user)
    current_app.logger.info('%s signup in successfully.', new_user.email)
    return new_user

def login_user(email:str, password:str, remember:bool=False) -> User:
    if not email:
        current_app.logger.info('User failed to login due to missed email.')
        raise MissingFields()
    user = get_user_by_email(email)
    if not user:
        current_app.logger.info('%s failed to log in.', user.email)
        raise EmailNotFound()
    if not check_password_hash(user.password, password):
        current_app.logger.info('%s failed to log in.', user.email)
        raise PasswordIncorrect()
    flask_login_user(user, remember)
    current_app.logger.info('%s logged in successfully.', user.email)
    return user

def logout_user() -> None:
    is_user_connected()
    flask_logout_user()
    current_app.logger.info('user logged out successfully.')

def oauth_user(name:str, email:str) -> User:
    if not email or not name:
        current_app.logger.info('User oauth failed due to missed information.')
        raise MissingFields()
    user = get_user_by_email(email)
    if user:
        flask_login_user(user)
        current_app.logger.info('%s logged successfully using OAuth.', user.email)
    else:
        user = User(email=email, name=name)
        db_insert(user)
        current_app.logger.info('%s signed up successfully using OAuth.', user.email)
    return user
