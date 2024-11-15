from flask import render_template

def get_index():
    return render_template('hello.html')
