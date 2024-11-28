from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def insert(o):
    db.session.add(o)
    commit()

def pop(o):
    db.session.delete(o)
    commit()

def commit():
    db.session.commit()
