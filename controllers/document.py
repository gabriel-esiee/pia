from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from flask_login import login_required
from werkzeug.exceptions import BadRequest, NotFound

from models.document_state import DocumentStateToString, StringToDocumentState

from services.document import get_document, create_document, edit_document, delete_document
from services.damage import get_damage

document_blueprint = Blueprint('document', __name__)

@document_blueprint.route('/<int:document_id>', methods=['GET'])
@login_required
def single(document_id):
    document = get_document(document_id)
    return render_template('document/single.html', document=document)

@document_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not request.args.get('damage'):
        raise NotFound
    damage_id = int(request.args.get('damage'))
    if request.method == 'GET':
        return render_template('document/new.html', damage_id=damage_id)
    elif request.method == 'POST':
        damage = get_damage(damage_id)
        description = request.form.get('description')
        data = request.form.get('file').encode('utf-8')
        try:
            create_document(damage, description, data)
        except BadRequest:
            flash('Please provide all mandatory fields to create the document.', 'error')
            return redirect(url_for("main.document.new", damage=damage_id))
        else:
            return redirect(url_for("main.damage.single", damage_id=damage.id))

@document_blueprint.route('/edit/<int:document_id>', methods=['GET', 'POST'])
@login_required
def edit(document_id):
    if request.method == 'GET':
        document = get_document(document_id)
        state_str = DocumentStateToString(document.state)
        return render_template('document/edit.html', document=document, document_state=state_str)
    elif request.method == 'POST':
        description = request.form.get('description')
        state = StringToDocumentState(request.form.get('state'))
        data = request.form.get('file').encode('utf-8')
        try:
            edit_document(document_id, description, state, data)
        except BadRequest:
            flash('Please provide all mandatory fields to edit the document.', 'error')
            return redirect(url_for("main.document.edit", document_id=document_id))
        else:
            return redirect(url_for('main.document.single', document_id=document_id))

@document_blueprint.route('/delete/<int:document_id>', methods=['GET'])
@login_required
def delete(document_id):
    document = get_document(document_id)
    associated_damage = document.damage.id
    delete_document(document)
    return redirect(url_for("main.damage.single", damage_id=associated_damage))
