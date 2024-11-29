from flask import render_template

def home_get():
    return render_template('index.html')
