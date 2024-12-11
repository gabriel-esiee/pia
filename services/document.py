from werkzeug.exceptions import NotFound, BadRequest

from services.user import is_user_connected, is_current_user_admin

from models.database import db_insert, db_pop, db_commit
from models.document import Document
from models.document_state import DocumentState
from models.damage import Damage

def get_document(id:int) -> Document:
    is_user_connected()
    document = Document.query.get(id)
    if not document:
        raise NotFound('Get document failed: document with id {id} not found')
    return document

def create_document(damage:Damage, description:str, data = None) -> Document:
    is_user_connected()
    if not damage or not description:
        raise BadRequest("Create new document failed: given informations are incorrect.")
    document = Document(description=description, data=data, damage=damage)
    db_insert(document)
    return document

def edit_document(id:int, description:str, state:DocumentState, data = None) -> Document:
    is_user_connected()
    if not id or not description or not state:
        raise BadRequest("Edit document failed: given informations are incorrect.")
    document = get_document(id)
    document.description = description
    document.state = state
    if data:
        document.data = data
    db_commit()
    return document

def delete_document(document:Document) -> None:
    is_current_user_admin()
    db_pop(document)

def delete_document_by_id(id:int) -> None:
    is_current_user_admin()
    document = get_document(id)
    db_pop(document)
