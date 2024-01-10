#!/usr/bin/python3
"""
create a view for the place review objects that handles all default RESTFul API actions

"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import abort, jsonify, request

@app_views.route('/place/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_place_review(place_id):
    """retrieve all reviews attribute of a place obj based of it id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_dict = []
    reviews = place.reviews
    for review in reviews:
        review_dict.append(review.to_dict())
    return jsonify(review_dict)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """retrieve the review based on its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['DELETE'])
def review_delete(review_id):
    """Delete review using its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=['POST'])
def review_place_post(place_id):
    """Create a new review of a place using its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json(force=True, silent=True)
    if not place_data:
        abort(400, "Not a JSON")
    user_id = place_data.get("user_id")
    if not user_id:
        abort(400, "Missing user_id")
    if storage.get(User, user_id) is None:
        abort(404)
    text = place_data.get("text")
    if not text:
        abort(400, "Missing text")
    
    new_review = Review(place_id=place.id, **place_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """update an existing review obj using its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data =  request.get_json(force=True, silent=True)
    if not review_data:
        abort(400, "Not a JSON")
    review.text = review_data.get("text", review.text)
    review.save()
    return jsonify(review.to_dict()), 200
