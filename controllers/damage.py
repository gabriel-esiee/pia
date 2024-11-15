from flask import render_template, redirect, url_for, abort
from flask_login import current_user
from app.models import add
from app.models.damage import Damage
from app.models.damageState import DamageState

def all_get():
    damages = Damage.query.all()
    return render_template('damage/list.html', title="All damages", damages=damages)

def unresolved_get():
    damages = Damage.query.filter(Damage.state != DamageState.CLOSED).all()
    return render_template('damage/list.html', title="All unclosed damages", damages=damages)

def one_get(damage_id):
    damage = Damage.query.get(damage_id)
    if damage:
        return render_template('damage/single.html', damage=damage)
    else:
        abort(404)

def new_get():
    return render_template('damage/new.html')

def new_post(form):
    description = form.get('description')
    new_damage = Damage(description=description, user=current_user)

    add(new_damage)
    
    return redirect(url_for('main.damage.all'))

