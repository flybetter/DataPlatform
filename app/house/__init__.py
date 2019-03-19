from flask import Blueprint
from flask import render_template, request, jsonify, session
from redis import Redis
import json
import pandas as pd
import numpy as np
import traceback
import hashlib

from app.tools.prpcrypt import PrpCrypt
from urllib import parse
from app.config import get_config
import re
import traceback

from app.tools import BuriedPoint

REDIS_HOST = get_config('REDIS_HOST')
REDIS_DB = get_config("REDIS_DB")

REMAIN_DAYS = get_config('REMAIN_DAYS')

FILE_NEWHOUSE_PATH = get_config('FILE_NEWHOUSE_PATH')
FILE_NEWHOUSELOG_PATH = get_config('FILE_NEWHOUSELOG_PATH')
FILE_NEWHOUSEROOM_PATH = get_config('FILE_NEWHOUSEROOM_PATH')
FILE_NEWHOUSEMODEL_PATH = get_config('FILE_NEWHOUSEMODEL_PATH')
FILE_SECONDHOUSE_PATH = get_config('FILE_SECONDHOUSE_PATH')
FILE_SECONDHOUSELOG_PATH = get_config('FILE_SECONDHOUSELOG_PATH')
FILE_BLOCK_PATH = get_config('FILE_BLOCK_PATH')
FILE_PHONEDEVICE_PATH = get_config("FILE_PHONEDEVICE_PATH")

REDIS_PHONEDEVICE_PREFIX = get_config("REDIS_PHONEDEVICE_PREFIX")
REDIS_NEWHOUSE_PREFIX = get_config('REDIS_NEWHOUSE_PREFIX')
REDIS_SECONDHOUSE_PREFIX = get_config('REDIS_SECONDHOUSE_PREFIX')

# CRM
REDIS_CRM_DB = get_config('REDIS_CRM_DB')
REDIS_CRM_HOST = get_config('REDIS_CRM_HOST')
REDIS_CRM_PREFIX = get_config('REDIS_CRM_PREFIX')
FILE_CRM_USER_PATH = get_config('FILE_CRM_USER_PATH')

from . import newhouse
from . import newhouseDetail

houses = Blueprint('houses', __name__, url_prefix='/houses')
houses_v1 = Blueprint('houses_v1', __name__, url_prefix='/v1/houses')

from . import housesController
from . import house
