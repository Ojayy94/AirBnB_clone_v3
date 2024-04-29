#!/usr/bin/python3
"""views"""
from flask import Blueprint


app_views = Blueprint('api_views', __name__, url_prefix='/api/vi')


from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
