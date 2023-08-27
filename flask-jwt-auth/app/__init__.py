import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from importlib import import_module

db = MongoClient(os.environ.get('MONGO_URI'))
jwt = JWTManager()
bcrypt = Bcrypt()

def register_blueprints(app):
    for module in ('auth', 'user'):
        module = import_module(f'app.{module}.routes')
        app.register_blueprint(module.blueprint)

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')
    print(app.config['MONGO_URI'])
    # Register extensions
    jwt.init_app(app)
    bcrypt.init_app(app)

    CORS(app)

    # Register bluepeints
    register_blueprints(app)

    return app
    