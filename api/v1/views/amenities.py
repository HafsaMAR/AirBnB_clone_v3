#!/usr/bin/python3
""" Amenities view that handles all default RESTful API actions"""

from models import storage
from models import amenity
from flask import jsonify, abort, request
from api.v1.views import app_views

@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
@app_views.route("/amenities/<amenities_id>", strict_slashes=False, methods=['GET'])
def amenities_get(amenities_id=None):
    """retrieve all or a amenity object"""
    amenity_dict = []
    if amenities_id is None:
        all_obj = storage.all(amenity).values()
        for value in all_obj:
            amenity_dict.append(value.to_dict())
        return jsonify(amenity_dict)
    
    else:
        amenities = storage.get(amenity, amenities_id)
        if amenities is None:
            abort(404)
        return jsonify(amenities.to_dict())


@app_views.route("/amenities/<amenities_id>", strict_slashes=False, methods=['DELETE'])
def amenities_delete(amenities_id):
    """Delete the amenity obj through its id"""
    amenity_obj = storage.get(amenity, amenities_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def amenity_post():
    """create a new amenity object"""
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    name = amenity_data.get('name')
    if name is None:
        abort(400, "Missing name")
    new_amenity = amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route("/amenities/<amenities_id>", strict_slashes=False, methods=["PUT"])
def amenities_put(amenities_id):
    """Update the amenity object"""
    amenity_obj = storage.get(amenity, amenities_id)
    if amenities_id is None:
        abort(404)
    amenity_data = request.get_json(force=True, silent=True)
    if not amenity_data:
        abort(400, "Not a JSON")
    amenity_obj.name = amenity_data.get("name", amenity_obj.name)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200