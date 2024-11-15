from flask import Blueprint
from app.controllers import get_index

index_blueprint = Blueprint('index_blueprint', __name__)

@index_blueprint.route('/')
def index():
    return get_index()
