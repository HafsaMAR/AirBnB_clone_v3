#!/usr/bin/python3
"""
create a view for the place amenity objects that handles all default RESTFul API actions
"""

from flask import abort, request,jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv

db_mode = getenv("HBNB_TYPE_STORAGE")

@app_views.route("/places/<place_id>/amenities", strict_slashes=False, methods=['GET'])
def Amenity_place_get(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity_dict =[]
    if db_mode == 'db':
        amenities = place.amenities
        for amenity in amenities:
            amenity_dict.append(amenity.to_dict())
    
    else:
        amenity_dict = place.amenity_ids
    return jsonify(amenity_dict)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=['DELETE'])
def amenity_place_delete(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or place is None:
        abort(404)
    if db_mode == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id
    
    for amenity in place_amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
        else:
            abort(404)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=['POST'])
def amenity_post(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or place is None:
        abort(404)
    if db_mode == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id
    
    if amenity not in place_amenities:
        place_amenities.append(amenity)
    else:
        return jsonify(amenity.to_dict()), 200
    return jsonify(amenity.to_dict()), 201
    
