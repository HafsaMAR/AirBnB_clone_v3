#!/usr/bin/python3

"""create a view for the city objects that handles all default RESTFul API actions"""

from flask import request, abort, jsonify
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def city_get(state_id=None):
    """Displays cities or city using its id"""
    city_dict = []
    state = storage.get(State, state_id)
    if state is None:
        all_cities = state.cities
        for cities in all_cities:
            city_dict.append(cities.to_dict())
        return jsonify(city_dict)



@app_views.route("cities/<city_id>", strict_slashes=False, methods=['GET'])
def city_get(city_id):
    """Displays cities or city using its id"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route("cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def city_delete(city_id):
    """delete city object using its id"""
    cities_obj = storage.get(City, city_id)
    if cities_obj is None:
        abort(404)
    storage.delete(cities_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=['POST'])
def city_post():
    """creates a new city and handle error request"""
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    name_city = city_data.get("name")
    if name_city is None:
        abort(400, 'Missing name')
    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def city_update(city_id):
    """update the existing cities"""
    city_obj = storage.get(City, city_id)
    if city_id is None:
        abort(404)
    
    city_data = request.get_json(force=True, silence=True)
    if not city_data:
        abort(400, "Not a JSON")
    city_obj.name = city_data.get("name", city_obj.name)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200

