from datetime import datetime
from flask import render_template, redirect, url_for, abort
from flask_login import current_user
from flask_babel import lazy_gettext

from models.database import db_insert, db_pop, db_commit
from models.damage import Damage
from models.damage_state import DamageState, DamageStateToString, StringToDamageState

def all_get():
    # Check that the user is authorized to manage damages
    if not current_user.is_admin():
        abort(403)
    else:
        # Fetch all damages of the database and render them inside a table
        damages = Damage.query.all()
        title = lazy_gettext('All damages')
        return render_template('damage/list.html', title=title, damages=damages)

def unresolved_get():
    # Check that the user is authorized to manage damages
    if not current_user.is_admin():
        abort(403)
    else:
        # Fetch all unresolved damages of the database and render them inside a table
        damages = Damage.query.filter(Damage.state != DamageState.CLOSED).all()
        title = lazy_gettext('All unresolved damages')
        return render_template('damage/list.html', title=title, damages=damages)

def single_get(damage_id):
    damage = Damage.query.get(damage_id)
    # If the requested id exist in the damage table, render the damage on a page
    if damage:
        return render_template('damage/single.html', damage=damage)
    # Else, return 404 error
    else:
        abort(404)

def new_get():
    return render_template('damage/new.html')

def new_post(form):
    # Get damage information from form data
    description = form.get('description')
    latitude = form.get('latitude')
    longitude = form.get('longitude')
    date = datetime.strptime(form.get('date'), '%Y-%m-%d')
    # Create new damage and insert into database
    new_damage = Damage(description=description, latitude=latitude, longitude=longitude, date=date, insured=current_user, impaired=current_user)
    db_insert(new_damage)
    # Redirect to the list of damages (depend on the role of the user) to see the new damage
    return redirect(url_for(current_user.list_endpoint()))

def edit_get(damage_id):
    damage = Damage.query.get(damage_id)
    if damage:
        return render_template('damage/edit.html', damage=damage, damage_state=DamageStateToString(damage.state))
    else:
        abort(404)

def edit_post(damage_id, form):
    damage = Damage.query.get(damage_id)
    damage.description = form.get('description')
    damage.latitude = form.get('latitude')
    damage.longitude = form.get('longitude')
    damage.state = StringToDamageState(form.get('state'))
    db_commit()
    return redirect(url_for('main.damage.single', damage_id=damage_id))

def delete_get(damage_id):
    # Check that the user is authorized to manage damages
    if not current_user.is_admin():
        abort(403)
    else:
        damage = Damage.query.get_or_404(damage_id)
        db_pop(damage)
        return redirect(url_for(current_user.list_endpoint()))
