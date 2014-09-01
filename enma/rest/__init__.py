from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/rest/v1.0')

from . import authentication, errors, views