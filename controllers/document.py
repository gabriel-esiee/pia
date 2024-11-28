from datetime import datetime
from flask import render_template, redirect, url_for, abort

from app.models.document import Document
from app.models.documentState import DocumentState

def single_get(document_id):
    document = Document.query.get(document_id)
    # If the requested id exist in the document table, render the document on a page
    if document:
        return render_template('document/single.html', document=document)
    # Else, return 404 error
    else:
        abort(404)
