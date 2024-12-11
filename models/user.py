from flask_login import UserMixin
from extensions import db
from models.user_role import UserRole

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(100))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.INSURED)
    
    def is_admin(self) -> bool:
        return self.role == UserRole.INVESTIGATOR
