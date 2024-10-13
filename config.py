import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_DEBUG=os.getenv('FLASK_DEBUG')
    FLASK_ENV=os.getenv('FLASK_ENV')
    FLASK_APP=os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False