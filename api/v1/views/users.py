#!/usr/bin/python3
"""
create a view for the User objects that handles all default RESTFul API actions

"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage

@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
@app_views.route("/users", strict_slashes=False, methods=['GET'])
def get_users(user_id=None):
    "Displays all object users or user using its id"
    if user_id is None:
        user_dict = []
        all_users = storage.all(User).values()
        for user in all_users:
            user_dict.append(user.to_dict())
        return jsonify(user_dict)
    
    else:
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404)
        return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['DELETE'])
def user_delete(user_id):
    user_obj = storage.get(User, user_id)
    if user_id is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def user_post():
    user_data = request.get_json(force=True, silent=True)
    if not user_data:
        abort(400, "Not a JSON")
    user_email = user_data.get("email")
    if not user_email:
        abort(400, "Missing email")
    user_pwd = user_data.get("password")
    if not user_pwd:
        abort(400, "Missing password")
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def user_update(user_id):
    """update the existing user object"""
    user_obj =storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    user_data = request.get_json(force=True, silent=True)
    if not user_data:
        abort(400, 'Not a JSON')
    user_obj.name = user_data.get("name", user_data.name)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
