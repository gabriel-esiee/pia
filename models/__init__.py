from app import database

def insert(o):
    database.session.add(o)
    commit()

def pop(o):
    database.session.delete(o)
    commit()

def commit():
    database.session.commit()
