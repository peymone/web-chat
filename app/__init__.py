# Third party packages
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

# BuidIn packagess
from os import getenv


# Load variables from env file
load_dotenv()

# Create SocketIO object for envoking events from client
socketio = SocketIO()

def create_app() -> Flask:
    """Create a Flask application"""
    
    # Get secret key for Flask sessions from env variable
    secter_key = getenv('SECRET')
    debug = getenv('DEBUG').lower()
        
    if (secter_key is None) or (debug is None): # Set default value if env is empty
        secter_key = '1f2c0d02be6d28090d0510b95a9d2661a5516e07a39da8cdb0b9ac9f1877'
        debug = True
    if isinstance(debug, str): # Variable from env is string type
        if debug == 'true': debug = True
        if debug == 'false': debug = False
            
    # Create and configurate Flask application
    app = Flask(__name__)
    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = secter_key

    # Register Flask blueprints
    from .auth import auth_bp
    from .chat import chat_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # Add Flask application to SocketIO object
    socketio.init_app(app)
    
    # Return Flask application
    return app