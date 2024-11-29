from flask import Blueprint, request
from flask_login import login_required
from controllers.damage import all_get, unresolved_get, single_get, new_get, new_post, edit_get, edit_post, delete_get

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
def single(damage_id):
    return single_get(damage_id)

@damage_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'GET':
        return new_get()
    elif request.method == 'POST':
        return new_post(request.form)
    
@damage_blueprint.route('/edit/<int:damage_id>', methods=['GET', 'POST'])
@login_required
def edit(damage_id):
    if request.method == 'GET':
        return edit_get(damage_id)
    elif request.method == 'POST':
        return edit_post(damage_id, request.form)

@damage_blueprint.route('/delete/<int:damage_id>', methods=['GET'])
@login_required
def delete(damage_id):
    return delete_get(damage_id)
