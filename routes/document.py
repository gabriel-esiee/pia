from flask import Blueprint
from flask_login import login_required
from app.controllers.document import single_get

document_blueprint = Blueprint('document', __name__)

@document_blueprint.route('/<int:document_id>', methods=['GET'])
@login_required
def single(document_id):
    return single_get(document_id)
