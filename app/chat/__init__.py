from flask import Blueprint

# Create Flask Blueprint object for routes
chat_bp = Blueprint('chat', __name__, template_folder='./templates', static_folder='./static')

from . import routes, events
