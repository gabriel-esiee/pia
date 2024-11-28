from flask_login import UserMixin
from app.models.database import db
from app.models.userRole import UserRole

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.INSURED)
    
    def is_admin(self) -> bool:
        return self.role == UserRole.INVESTIGATOR
    
    def list_endpoint(self) -> str:
        if self.is_admin():
            return 'main.damage.all'
        else:
            return 'main.user.damages'