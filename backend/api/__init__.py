from flask import Blueprint

# Create API blueprint
api_blueprint = Blueprint('api', __name__)

# Import API routes
from api.v1 import *
