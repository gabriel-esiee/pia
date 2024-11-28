import json
from flask import Flask, request, render_template
from flask_babel import Babel
from flask_login import LoginManager

from app import oauth
from app.routes.home import main_blueprint
from app.models.database import db
from app.models.user import User

# Create Flask application
app = Flask(__name__, template_folder='templates')
app.config.from_file(f"config.json", load=json.load)
app.register_blueprint(main_blueprint)

# Listen for errors
@app.errorhandler(403)
def resource_forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def resource_not_found(error):
    return render_template('404.html'), 404

# Initialize to database
db.init_app(app)
with app.app_context(): db.create_all()

# Initialize Babel module
def get_locale():
    # Choose locale based on the Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])
babel = Babel()
babel.init_app(app, locale_selector=get_locale)

# Initialize login manager
login = LoginManager()
login.login_view = 'main.user.login'
login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize OAuth
app.config['GOOGLE_CLIENT_ID'] = '72701988235-3bqpnaugrhnl6ktte3ub4i6le7osc9lg.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'
oauth.init_app(app)
