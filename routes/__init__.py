from flask import Blueprint
from app.routes.user import user_blueprint
from app.controllers import get_index

main_blueprint = Blueprint('main', __name__, template_folder='templates')

main_blueprint.register_blueprint(user_blueprint, url_prefix='/user')

@main_blueprint.route('/')
def index():
    return get_index()
