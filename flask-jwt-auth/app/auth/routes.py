from flask import jsonify, request
from flask_jwt_extended import create_access_token
from http import HTTPStatus

from app import db, bcrypt

from . import blueprint


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def verify_password(hashed_password, plain_password):
    return bcrypt.check_password_hash(hashed_password, plain_password)


# Signup route to add new users
@blueprint.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), HTTPStatus.BAD_REQUEST

    existing_user = db.db.users_auth.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), HTTPStatus.CONFLICT
    
    hashed_password = hash_password(password)
    db.db.users_auth.insert_one({'username': username, 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'}), HTTPStatus.CREATED


# Login route 
@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.db.users_auth.find_one({'username': username})
    if user and verify_password(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), HTTPStatus.OK
    
    return jsonify({'message': 'Invalid credentials'}), HTTPStatus.UNAUTHORIZED