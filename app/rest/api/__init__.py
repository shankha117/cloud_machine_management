from flask import Blueprint

cloud_manager = Blueprint('routes', __name__, url_prefix='/cmm/api/v1')

from .cluster import *
from .instance import *
