# Flask application initialization

from flask import Flask, request, render_template

from .config import Config
from app.routes import main_blueprint

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
app.register_blueprint(main_blueprint)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Flask-Babel initialization

from flask_babel import Babel

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES']) # Choose locale based on the Accept-Language header

babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

# Flask-SQLAlchemy initialization
from app import database
from flask_login import LoginManager
from app.models.user import User

database.init_app(app)

with app.app_context():
    database.create_all()

login_manager = LoginManager()
login_manager.login_view = 'main.user.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))