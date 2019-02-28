from flask import Blueprint

secondhouses = Blueprint('secondhouses', __name__, url_prefix='/secondhouses')

from . import secondhouseController
