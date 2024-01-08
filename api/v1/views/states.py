#!/usr/bin/python3
""""""
from flask import Flask, request, jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views



@app_views.route('/states', strict_slashes=False, Methods=['GET'])
@app_views.route("states/<state_id>")
def get_states(state_id=None):
    """Displays states or state with id"""
    state_dict = []
    if state_id is None:
        all_obj = storage.all(State).values()
        for value in all_obj:
            state_dict.append(value.to_dict())
        return jsonify(state_dict)
    
    else:
        states = storage.get(State, state_id)
        if states is None:
            abort(404)
        return jsonify(states.to_dict())

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def states_delete(state_id):
    "delete the state based state_id"
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", strict_slashes=False, methods=['POST'])
def state_post():
    """Creates a new state and handle error request"""
    """check if the returned date is JSON"""
    state_data = request.get_json()
    if not state_data:
        """raise error data is not JSON"""
        raise ValueError("Not a JSON")
    name = state_data.get('name')
    if not name:
        raise ValueError('Missing name')
    new_state = State(*state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def state_update(state_id):
    """update the existing states"""
    """check whether the state_id exists"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    state_obj.name = data.get("name", state_obj.name)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
    
