#!/usr/bin/python3
"""Place API"""
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place).values()
    places_list = [place.to_dict() for place in places
                   if place.city_id == city_id]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    if "user_id" not in data:
        abort(400, description='Missing user_id')
    if "name" not in data:
        abort(400, description='Missing name')

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)
