from flask import Blueprint

# Create Flask Blueprint object for routes
auth_bp = Blueprint('auth', __name__, template_folder='./templates')

from . import routes
