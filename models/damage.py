from datetime import datetime
from app import database
from app.models.damageState import DamageState

class Damage(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.String(1000))
    state = database.Column(database.Enum(DamageState), nullable=False, default=DamageState.STARTED)
    latitude = database.Column(database.Numeric(precision=15, scale=10), default=0.0)
    longitude = database.Column(database.Numeric(precision=15, scale=10), default=0.0)
    date = database.Column(database.DateTime, default=datetime.now())
    insured_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    impaired_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    insured = database.relationship('User', foreign_keys=[insured_id], backref=database.backref('insured_damages', lazy=True))
    impaired = database.relationship('User', foreign_keys=[impaired_id], backref=database.backref('impaired_damages', lazy=True))