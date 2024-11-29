from datetime import datetime
from extensions import db
from models.damage_state import DamageState

class Damage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    state = db.Column(db.Enum(DamageState), nullable=False, default=DamageState.STARTED)
    latitude = db.Column(db.Numeric(precision=15, scale=10), default=0.0)
    longitude = db.Column(db.Numeric(precision=15, scale=10), default=0.0)
    date = db.Column(db.DateTime, default=datetime.now())
    insured_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    impaired_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    insured = db.relationship('User', foreign_keys=[insured_id], backref=db.backref('insured_damages', lazy=True))
    impaired = db.relationship('User', foreign_keys=[impaired_id], backref=db.backref('impaired_damages', lazy=True))