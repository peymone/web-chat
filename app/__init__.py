# Third party packages
from flask import Flask
from flask_socketio import SocketIO

from os import getenv

# Create SocketIO object for envoking events from client
socketio = SocketIO()


def create_app(debug=False) -> Flask:
    """Create a Flask application"""
    
    # Get secret key for Flask sessions from env variable
    secter_key = getenv('SECRET')
    if secter_key is None:
        secter_key = 'TOP_SECRET12345' # Default value if env is empty
    
    # Create and configurate Flask application
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = secter_key

    # Register Flask blueprints
    from .auth import auth_bp
    from .chat import chat_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    # Add Flask application to SocketIO object
    socketio.init_app(app)
    
    # Return Flask application
    return app