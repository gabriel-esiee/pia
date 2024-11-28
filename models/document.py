from datetime import datetime
from app.models.database import db
from app.models.documentState import DocumentState

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String(1000))
    state = db.Column(db.Enum(DocumentState), nullable=False, default=DocumentState.REQUESTED)
    data = db.Column(db.LargeBinary)
    damage_id = db.Column(db.Integer, db.ForeignKey('damage.id'), nullable=False)

    damage = db.relationship('Damage', foreign_keys=[damage_id], backref=db.backref('documents', lazy=True))
