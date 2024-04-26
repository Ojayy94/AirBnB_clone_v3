#!/usr/bin/python3
"""views"""

from flask import Blueprint

app_views = Blueprint('api_views', __name__, url_prefix='/api/vi')

from api.v1.views.index import *
