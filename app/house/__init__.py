from flask import Blueprint

houses = Blueprint('houses', __name__, url_prefix='/houses')

from . import house
