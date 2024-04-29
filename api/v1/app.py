#!/usr/bin/python3
""" Flask Application """

from models import storage
from api.v1.views import app_views
from flask import Flask, abort, jsonify
from flask import make_response, render_template
from os import getenv, environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(self):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """calls the function"""
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
             port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
