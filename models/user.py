from app import database
from flask_login import UserMixin
from app.models.userRole import UserRole

class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(100), unique=True)
    password = database.Column(database.String(100))
    name = database.Column(database.String(100))
    role = database.Column(database.Enum(UserRole), nullable=False, default=UserRole.INSURED)
