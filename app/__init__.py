from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

swagger = Swagger()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    
    CORS(app)
    
    jwt.init_app(app)
    
    swagger.init_app(app)
    
    ma.init_app(app)
    
    from .routes import api_bp
    from .auth import auth_bp
    from .utils import swaggerui_blueprint

    from .models import User, Item
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    app.register_blueprint(api_bp, url_prefix='/api')
    
    app.register_blueprint(swaggerui_blueprint)

    return app
