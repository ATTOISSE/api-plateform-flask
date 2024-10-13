from marshmallow import fields
from .models import User, Item
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True 

    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True) 
    role = fields.Str(required=True) 

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True

    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True)
    price = fields.Int(required=True)
    description = fields.Str()
    user_id = fields.Int(required=True)

