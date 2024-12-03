from flask import Flask, request, session, render_template
from logging.config import dictConfig

from extensions import db
from extensions import login_manager
from extensions import oauth
from extensions import babel

from routes.home import main_blueprint
from models.user import User

# Configure logging system.

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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

# Babel initialization.

def get_locale():
    return session.get('language', request.accept_languages.best_match(app.config['LANGUAGES']))

babel.init_app(app, locale_selector=get_locale)

# Login manager initialization.

login_manager.init_app(app)
login_manager.login_view = 'main.user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# OAuth initialization.

oauth.init_app(app)

# Start the application.

if __name__ == "__main__":
    import os
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host='0.0.0.0', port=port)
