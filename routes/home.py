from flask import Blueprint
from routes.user import user_blueprint
from routes.damage import damage_blueprint
from routes.document import document_blueprint
from controllers.home import home_get

main_blueprint = Blueprint('main', __name__, template_folder='templates')

main_blueprint.register_blueprint(user_blueprint, url_prefix='/')
main_blueprint.register_blueprint(damage_blueprint, url_prefix='/damage')
main_blueprint.register_blueprint(document_blueprint, url_prefix='/document')

@main_blueprint.route('/')
def index():
    return home_get()
