#!/usr/bin/python3
"""Create an endpoint that retrieves the number of each objects by type"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Routing"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def count():
    """Create an endpoint that retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    counts = {}
    for num in range(len(classes)):
        counts[names[num]] = storage.count(classes[num])

    return jsonify(counts)
