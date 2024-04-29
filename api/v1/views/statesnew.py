#!/usr/bin/python3
"""States API"""
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """"Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = []
    for i in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    return jsonify(states.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a State"""
    states = storage.get(State, state_id)
    if not states:
        abort(404)

    storage.delete(states)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state"""
    if not request.get_json():
        abort(400, description='Not a JSON')

    if "name" not in request.get_json():
        abort(400, description='Missing name')

    input_data = request.get_json()
    create = State(**input_data)
    create.save()
    return make_response(jsonify(create.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state():
    """update a state"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)
    if not request.is_json():
        abort(400, description='Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']

    input_data = request.get_json()
    for k, v in input_data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
