from flask import Blueprint, request 
from app import db
from app.models import User
from app.schemas import UserSchema
from app.error import success_response, handle_db_error, handle_validation_error
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])  
def register():
    data = request.get_json()
    role = data.get('role', 'user')  
    try:
        user = user_schema.load(data, session=db.session)
        user.set_password(data['password'])
        user.role = role  
        db.session.add(user)
        db.session.commit()
        return success_response(data=user_schema.dump(user), message="Utilisateur créé avec succès", code=201)
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)
    except ValidationError as ve:
        return handle_validation_error(ve)

@auth_bp.route('/login', methods=['POST'])  
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={"id": user.id, "role": user.role})  
        return success_response(data={'access_token': access_token}, message="Connexion réussie", code=200)
    return {"msg": "Identifiants invalides"}, 401
