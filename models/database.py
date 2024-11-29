from extensions import db

def db_insert(o):
    db.session.add(o)
    db_commit()

def db_pop(o):
    db.session.delete(o)
    db_commit()

def db_commit():
    db.session.commit()
