from datetime import datetime
from flask import render_template, redirect, url_for, abort
from flask_login import current_user
from app.models import insert, pop, commit
from app.models.damage import Damage
from app.models.damageState import DamageState, StateToString, StringToState

def all_get():
    damages = Damage.query.all()
    return render_template('damage/list.html', title="All damages", damages=damages, back_page='main.damage.all')

def unresolved_get():
    damages = Damage.query.filter(Damage.state != DamageState.CLOSED).all()
    return render_template('damage/list.html', title="All unclosed damages", damages=damages, back_page='main.damage.all')

def single_get(damage_id):
    damage = Damage.query.get(damage_id)
    if damage:
        return render_template('damage/single.html', damage=damage)
    else:
        abort(404)

def new_get():
    return render_template('damage/new.html')

def new_post(form):
    description = form.get('description')
    latitude = form.get('latitude')
    longitude = form.get('longitude')
    date = datetime.strptime(form.get('date'), '%Y-%m-%d')

    try:
        latitude = float(latitude)
    except ValueError:
        latitude = 0.0
        print('Cannot convert latitude to string!')

    try:
        longitude = float(longitude)
    except ValueError:
        longitude = 0.0
        print('Cannot convert longitude to string!')

    new_damage = Damage(description=description, latitude=latitude, longitude=longitude, date=date, insured=current_user, impaired=current_user)
    insert(new_damage)
    
    return redirect(url_for('main.damage.all'))

def edit_get(damage_id):
    damage = Damage.query.get(damage_id)
    if damage:
        damage_state = StateToString(damage.state)
        return render_template('damage/edit.html', damage=damage, damage_state=damage_state)
    else:
        abort(404)

def edit_post(damage_id, form):
    damage = Damage.query.get(damage_id)
    damage.description = form.get('description')
    damage.latitude = form.get('latitude')
    damage.longitude = form.get('longitude')
    damage.state = StringToState(form.get('state'))
    commit()
    return redirect(url_for('main.damage.single', damage_id=damage_id))

def delete_get(damage_id):
    damage = Damage.query.get_or_404(damage_id)
    pop(damage)
    return redirect(url_for('main.damage.all'))
