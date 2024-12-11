from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest
from flask_login import current_user

from services.user import is_user_connected, is_current_user_admin

from models.database import db_insert, db_pop, db_commit
from models.damage import Damage
from models.damage_state import DamageState

def get_all_damages() -> list:
    is_current_user_admin()
    # Return all damages of the database
    damages = Damage.query.all()
    return damages

def get_all_unresolved() -> list:
    is_current_user_admin()
    # Return all damages of the database
    damages = Damage.query.filter(Damage.state != DamageState.CLOSED).all()
    return damages

def get_damage(id:int) -> Damage:
    damage = Damage.query.get(id)
    if not damage:
        raise NotFound('Get damage failed: damage with id {id} not found')
    return damage

def create_damage(date:datetime, description:str, latitude:float, longitude:float) -> Damage:
    is_user_connected()
    # Check given informations are correct
    if not date or not description or not latitude or not longitude:
        raise BadRequest("Create new damage failed: given informations are incorrect.")
    # Create new damage and insert into database
    new_damage = Damage(description=description, latitude=latitude, longitude=longitude, date=date, insured=current_user, impaired=current_user)
    db_insert(new_damage)
    # Return the id of the created damage
    return new_damage

def edit_damage(id:int, description:str, latitude:float, longitude:float, state:DamageState) -> Damage:
    is_user_connected()
    # Check given informations are correct
    if not description or not latitude or not longitude or not state:
        raise BadRequest("Edit damage failed: given informations are incorrect.")
    # Get damage to edit (raise 404 if not found)
    damage = get_damage(id)
    damage.description = description
    damage.latitude = latitude
    damage.longitude = longitude
    damage.state = state
    db_commit()
    return damage

def delete_damage(id:int) -> None:
    is_current_user_admin()
    # Get and delete the damage
    damage = get_damage(id)
    db_pop(damage)
