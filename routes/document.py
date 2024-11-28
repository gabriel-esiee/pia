from flask import Blueprint, request
from flask_login import login_required
from app.controllers.document import single_get, new_get, new_post, edit_get, edit_post, delete_get

document_blueprint = Blueprint('document', __name__)

@document_blueprint.route('/<int:document_id>', methods=['GET'])
@login_required
def single(document_id):
    return single_get(document_id)

@document_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    damage_arg = request.args.get('damage')
    if damage_arg:
        damage_id = int(damage_arg)
        if request.method == 'GET':
            return new_get(damage_id)
        elif request.method == 'POST':
            return new_post(request.form, damage_id)
    # else:
        # abort(404)

@document_blueprint.route('/edit/<int:document_id>', methods=['GET', 'POST'])
@login_required
def edit(document_id):
    if request.method == 'GET':
        return edit_get(document_id)
    elif request.method == 'POST':
        return edit_post(document_id, request.form)

@document_blueprint.route('/delete/<int:document_id>', methods=['GET'])
@login_required
def delete(document_id):
    return delete_get(document_id)
