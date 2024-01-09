#!/usr/bin/python3

"""
create a view for the places objects that handles
all default RESTful API actions

"""

from flask import request, abort, jsonify
from models import storage
from api.v1.views import app_views
from models.user import User
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=['GET'])
def place_city_get(city_id):
    """Display all object places"""
    place_dict = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = city.places
    for place in all_places:
        place_dict.append(place.to_dict())
    return jsonify(place_dict)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['GET'])
def place_get(place_id):
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def place_user(place_id):
    """Delete the places object using its id"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def place_post(city_id):
    """Create a new place and handle error request"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    place_data = request.get_json(force=True, silent=True)
    if not place_data:
        abort(400, "Not a JSON")
    place_user = place_data.get("user_id")
    if not place_user:
        abort(400, "Missing user_id")
    if storage.get(User, place_user) is None:
        abort(404)
    place_name = place_data.get("name")
    if not place_name:
        abort(400, 'Missing name')
    new_place = Place(city_id=city_obj.id, **place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """update place object using id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json(force=True, silent=True)
    if not place_data:
        abort(400, "Not a JSON")
    place.name = place_data.get("name", place.name)
    place.description = place_data.get("description", place.description)
    place.number_rooms = place_data.get("number_rooms", place.number_rooms)
    place.number_bathrooms = place_data.get("number_bathrooms",
                                            place.number_bathrooms)
    place.max_guest = place_data.get("max_guest", place.max_guest)
    place.price_by_night = place_data.get("price_by_night",
                                          place.price_by_night)
    place.latitude = place_data.get("latitude", place.latitude)
    place.longitude = place_data.get("longitude", place.longitude)
    place.save()
    return jsonify(place.to_dict()), 200
