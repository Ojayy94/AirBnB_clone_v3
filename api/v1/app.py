#!/usr/bin/python3
""" Flask Application """

from models import storage
from api.v1.views import app_views
from flask import Flask, abort, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(self):
    """close"""
    storage.close()


if __name__ == "__main__":
    """calls the function"""
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
