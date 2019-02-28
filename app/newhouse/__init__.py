from flask import Blueprint

newhouses = Blueprint('newhouses', __name__, url_prefix='/newhouses')

from . import newhouseController
