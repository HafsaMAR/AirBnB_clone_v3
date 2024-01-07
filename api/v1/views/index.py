#!/usr/bin/python3
"""Define routes of blueprint"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

@app_views.route('/status', strict_slashes=False, methods=["GET"])
def status():
    return jsonify(status="OK")

@app_views.route('/stats', strict_slashes=False, methods=["GET"])
def get_stats():
    stats = {
        "Amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "state": storage.count(State),
        "users": storage.count(User)
        }