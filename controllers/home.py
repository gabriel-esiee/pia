from flask import render_template, redirect, url_for, session, request

def home_get():
    return render_template('index.html')

def language_get(language):
    from config import LANGUAGES
    if language in LANGUAGES:
        session['language'] = language
    return redirect(request.referrer or url_for('main.home'))