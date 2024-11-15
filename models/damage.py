from app import database
from app.models.damageState import DamageState

class Damage(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.String(1000))
    state = database.Column(database.Enum(DamageState), nullable=False, default=DamageState.STARTED)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    user = database.relationship('User', backref=database.backref('damages', lazy=True))