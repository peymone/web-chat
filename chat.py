# BuildIn packages
from os import getenv
from argparse import ArgumentParser

# My modules
from app import create_app, socketio
from app.database import create_db, add_chat


# Parse cli arguments
parser = ArgumentParser()
parser.add_argument("-s", "--start", help="Start application", type=bool)
parser.add_argument("-c", "--chat", help="Add new chat to database", type=bool)
args = parser.parse_args()
args_set = set([args.start, args.chat])

# Create database
creation_result = create_db()
print("Database creation result: ", creation_result[1])

# Create default chat room
add_chat(name="common", description="everybody here")

# Start application
if args.start or (len(args_set) == 1 and None in args_set):

    # Create Flask application
    app = create_app()
    
    # Get host and port from '.env' file
    host = getenv('HOST')
    port = getenv('PORT')

    # Start application with specified host and port or with default values
    if app.debug == True:
        socketio.run(app) # localhost:5000
    elif ([host, port]):
        socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True) # Specified in '.env'
    else:
        socketio.run(app) # localhost:5000

if args.chat: # Add new chat room to database
    name = input("Enter chat name: ")
    desc = input("Enter chat description: ")
    password = input("Enter paswword (optional - click enter to pass): ")
    
    if len(password) == 0:
        password = None
    
    res = add_chat(name, desc, password)
    print(res[1])