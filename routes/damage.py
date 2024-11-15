from flask import Blueprint, request
from flask_login import login_required
from app.controllers.damage import all_get, unresolved_get, one_get, new_get, new_post

damage_blueprint = Blueprint('damage', __name__)

@damage_blueprint.route('/all', methods=['GET'])
@login_required
def all():
    return all_get()

@damage_blueprint.route('/unresolved', methods=['GET'])
@login_required
def unresolved():
    return unresolved_get()

@damage_blueprint.route('/<int:damage_id>', methods=['GET'])
def one(damage_id):
    return one_get(damage_id)

@damage_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'GET':
        return new_get()
    elif request.method == 'POST':
        return new_post(request.form)