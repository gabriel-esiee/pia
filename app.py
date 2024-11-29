from flask import Flask, request, render_template

from extensions import db
from extensions import login_manager
from extensions import oauth
from extensions import babel

from routes.home import main_blueprint
from models.user import User

# Create Flask application.

app = Flask(__name__, template_folder='templates')
app.config.from_pyfile(f"config.py")

app.register_blueprint(main_blueprint)

# Handle errors.

@app.errorhandler(403)
def resource_forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def resource_not_found(error):
    return render_template('404.html'), 404

# Database initialization.

db.init_app(app)

with app.app_context(): db.create_all()

# Babel initialization?

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel.init_app(app, locale_selector=get_locale)

# Login manager initialization.

login_manager.init_app(app)
login_manager.login_view = 'main.user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# OAuth initialization.

app.config['GOOGLE_CLIENT_ID'] = '72701988235-3bqpnaugrhnl6ktte3ub4i6le7osc9lg.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'

oauth.init_app(app)
