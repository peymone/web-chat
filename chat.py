# BuildIn packages
from os import getenv

# My modules
from app import create_app, socketio
from app.database import create_db


# Create database
creation_result = create_db()

# Create Flask application
app = create_app()

if __name__ == '__main__':
    host = getenv('HOST')
    port = getenv('PORT')

    if all((host, port)):
        socketio.run(host=host, port=port)
    else:
        socketio.run(app)