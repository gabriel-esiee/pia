from flask import Blueprint, request, render_template, redirect, url_for

from services.language import change_lang

from controllers.damage import damage_blueprint
from controllers.document import document_blueprint
from controllers.user import user_blueprint

main_blueprint = Blueprint('main', __name__, template_folder='templates')

main_blueprint.register_blueprint(user_blueprint, url_prefix='/')
main_blueprint.register_blueprint(damage_blueprint, url_prefix='/damage')
main_blueprint.register_blueprint(document_blueprint, url_prefix='/document')

@main_blueprint.route('/')
def home():
    return render_template('index.html')

@main_blueprint.route('/language/<language>')
def language(language):
    change_lang(lang=language)
    return redirect(request.referrer or url_for('main.home'))
