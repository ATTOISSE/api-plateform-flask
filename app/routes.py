from flask import Blueprint, request 
from app import db
from app.models import User, Item
from app.schemas import UserSchema, ItemSchema
from app.error import success_response, handle_db_error, handle_validation_error
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort

api_bp = Blueprint('api', __name__)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.get(current_user['id'])  
            if user.role != role:
                abort(403)  
            return fn(*args, **kwargs)
        return decorator
    return wrapper

user_schema = UserSchema()
users_schema = UserSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@api_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = user_schema.load(data, session=db.session)
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return success_response(data=user_schema.dump(user), message="Utilisateur créé avec succès", code=201)
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)  
    except ValidationError as ve:
        return handle_validation_error(ve)  

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return success_response(data=users_schema.dump(users)), 200

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return success_response(data=user_schema.dump(user)), 200

@api_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    try:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return success_response(data=user_schema.dump(user)), 200
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)  
    except ValidationError as ve:
        return handle_validation_error(ve)  

@api_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return success_response(message='Utilisateur supprimé avec succès', code=204)

@api_bp.route('/item', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_item():
    data = request.get_json()
    try:
        item = item_schema.load(data, session=db.session)
        db.session.add(item)
        db.session.commit()
        return success_response(data=item_schema.dump(item), message="Élément créé avec succès", code=201)
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)  
    except ValidationError as ve:
        return handle_validation_error(ve)  

@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return success_response(data=items_schema.dump(items)), 200

@api_bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return success_response(data=item_schema.dump(item)), 200

@api_bp.route('/items/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    item.description = data.get('description', item.description)
    db.session.commit()
    return success_response(data=item_schema.dump(item)), 200

@api_bp.route('/items/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return success_response(message='Élément supprimé avec succès', code=204)



