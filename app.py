from flask import Flask, request, render_template
from .config import Config
from flask_babel import Babel, gettext
from app.routes import blueprint

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
app.register_blueprint(blueprint)

def get_locale():
    # Choose the best matching locale, based on the Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404