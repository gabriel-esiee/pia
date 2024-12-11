from flask import session
from config import LANGUAGES

def change_lang(lang):
    if lang in LANGUAGES:
        session['language'] = lang
