from app import database

def add(o):
    database.session.add(o)
    database.session.commit()