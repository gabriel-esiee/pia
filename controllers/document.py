from datetime import datetime
from flask import render_template, redirect, url_for, abort
from flask_login import current_user

from app.models.database import insert, pop, commit
from app.models.document import Document
from app.models.damage import Damage
from app.models.documentState import DocumentState, StateToString, StringToState

def single_get(document_id):
    document = Document.query.get_or_404(document_id)
    # If the requested id exist in the document table, render the document on a page
    return render_template('document/single.html', document=document)

def new_get(damage_id):
    return render_template('document/new.html', damage_id=damage_id)

def new_post(form, damage_id):
    damage = Damage.query.get_or_404(damage_id)
    
    # If the requested damage exist in the damage table, render the damage on a page
    description = form.get('description')
    data = form.get('file').encode('utf-8')
    
    # Create new damage and insert into database
    new_document = Document(description=description, data=data, damage=damage)
    insert(new_document)
    
    # Redirect to the list of damages (depend on the role of the user) to see the new damage
    return redirect(url_for("main.damage.single", damage_id=damage.id))

def edit_get(document_id):
    document = Document.query.get_or_404(document_id)
    return render_template('document/edit.html', document=document, document_state=StateToString(document.state))

def edit_post(document_id, form):
    damage = Document.query.get_or_404(document_id)
    damage.description = form.get('description')
    damage.data = form.get('file').encode('utf-8')
    damage.state = StringToState(form.get('state'))
    commit()
    return redirect(url_for('main.document.single', document_id=document_id))


def delete_get(document_id):
    # Check that the user is authorized to manage damages
    if not current_user.is_admin():
        abort(403)
    else:
        print("Fetching document.")
        print(document_id)
        document = Document.query.get_or_404(document_id)
        associated_damage = document.damage.id
        print("Deleting document.")
        pop(document)
        return redirect(url_for("main.damage.single", damage_id=associated_damage))
