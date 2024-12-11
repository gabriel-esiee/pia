from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from flask_babel import lazy_gettext

from models.damage_state import DamageStateToString, StringToDamageState

from services.damage import create_damage, edit_damage, delete_damage
from services.damage import get_damage, get_all_damages, get_all_unresolved

damage_blueprint = Blueprint('damage', __name__)

@damage_blueprint.route('/all', methods=['GET'])
@login_required
def all():
    damages = get_all_damages()
    title = lazy_gettext('All damages')
    return render_template('damage/list.html', title=title, damages=damages)

@damage_blueprint.route('/unresolved', methods=['GET'])
@login_required
def unresolved():
    damages = get_all_unresolved()
    title = lazy_gettext('All unresolved damages')
    return render_template('damage/list.html', title=title, damages=damages)

@damage_blueprint.route('/<int:damage_id>', methods=['GET'])
def single(damage_id):
    damage = get_damage(damage_id)
    return render_template('damage/single.html', damage=damage)

@damage_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'GET':
        return render_template('damage/new.html')
    elif request.method == 'POST':
        # Get damage information from form data
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        # Create new damage and insert into database
        damage = create_damage(date, description, latitude, longitude)
        return redirect(url_for('main.damage.single', damage_id=damage.id))

@damage_blueprint.route('/edit/<int:damage_id>', methods=['GET', 'POST'])
@login_required
def edit(damage_id):
    if request.method == 'GET':
        damage = get_damage(damage_id)
        state_str = DamageStateToString(damage.state)
        return render_template('damage/edit.html', damage=damage, damage_state=state_str)
    elif request.method == 'POST':
        description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        state = StringToDamageState(request.form.get('state'))
        updated_damage = edit_damage(damage_id, description, latitude, longitude, state)
        return redirect(url_for('main.damage.single', damage_id=updated_damage.id))

@damage_blueprint.route('/delete/<int:damage_id>', methods=['GET'])
@login_required
def delete(damage_id):
    delete_damage(damage_id)
    return redirect(url_for('main.user.damages'))
