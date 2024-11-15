from flask import render_template
from app.models.user import User

def get_index():
    myUser = User()
    return render_template('user/index.html', username=myUser.getName())

def get_login():
    return render_template('user/login.html')