from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from app.models.database import insert
from app.models.user import User

def signup_get():
    return render_template('user/signup.html')

def signup_post(form):
    email = form.get('email')
    name = form.get('name')
    password = form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('main.user.signup'))

    hash = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, name=name, password=hash)
    insert(new_user)

    return redirect(url_for('main.user.login'))

def login_get():
    return render_template('user/login.html')

def login_post(form):
    email = form.get('email')
    password = form.get('password')
    remember = True if form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.user.login'))

    login_user(user, remember=remember)
    
    return redirect(url_for('main.user.profile'))

def logout_get():
    logout_user()
    return redirect(url_for('main.user.login'))

def profile_get():
    return render_template('user/profile.html')

def damages_get():
    return render_template('damage/list.html', title="All your damages", damages=current_user.insured_damages)
