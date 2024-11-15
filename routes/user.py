from flask import Blueprint
from app.controllers.user import get_index, get_login

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/')
def index():
    
    return get_index()

@user_blueprint.route('/login')
def login():
    return get_login()
