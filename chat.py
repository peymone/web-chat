# My modules
from app import create_app, socketio
from app.database import create_db


# Create database
creation_result = create_db()
print(creation_result[1])

# Create Flask application
app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)