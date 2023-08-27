from flask import jsonify, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app import db

from . import blueprint

class User:
    def __init__(self, user_id, name, username):
        self.user_id = user_id
        self.name = name
        self.username = username


@blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users_collection = db.db.users_data
    users = users_collection.find({}, {"_id": 0})
    user_list = [user for user in users]
    return jsonify(user_list), HTTPStatus.OK


@blueprint.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    users_collection = db.db.users_data
    user = users_collection.find_one({"user_id": user_id}, {"_id": 0})
    if user:
        return jsonify(user), HTTPStatus.OK
    else:
        return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND


@blueprint.route('/user', methods=['POST'])
@jwt_required()
def add_user():
    name = request.form.get('name')
    username = request.form.get('username')
    
    if not name or not username:
        return jsonify({"message": "Name and username are required fields"}), 400
    
    users_collection = db.db.users_data
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "Username already exists"}), HTTPStatus.CONFLICT
    
    user_id = users_collection.count_documents({}) + 1
    new_user = User(user_id, name, username)
    users_collection.insert_one(new_user.__dict__)
    return jsonify({"message": "User added successfully"}), HTTPStatus.CREATED


@blueprint.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    name = request.form.get('name')
    username = request.form.get('username')
    
    users_collection = db.db.users_data
    user = users_collection.find_one({"user_id": user_id})
    if user:
        user['name'] = name
        user['username'] = username
        users_collection.update_one({"user_id": user_id}, {"$set": user})
        return jsonify({"message": "User updated successfully"}), HTTPStatus.OK
    else:
        return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND


@blueprint.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    users_collection = db.db.users_data
    user = users_collection.find_one({"user_id": user_id})
    if user:
        users_collection.delete_one({"user_id": user_id})
        return jsonify({"message": "User deleted successfully"}), HTTPStatus.OK
    else:
        return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND