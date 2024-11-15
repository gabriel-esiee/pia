from flask import Blueprint

blueprint = Blueprint('blueprint', __name__, template_folder='templates')

from .index import index_blueprint

blueprint.register_blueprint(index_blueprint, url_prefix='/')

from .user import user_blueprint

blueprint.register_blueprint(user_blueprint, url_prefix='/user')
