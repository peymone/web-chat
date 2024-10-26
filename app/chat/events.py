# Third party packages
from flask_socketio import join_room, leave_room, send, emit
from flask import session, request

from datetime import datetime

# My modules
from .. import socketio
from ..database import add_message, get_messages


# Configuration variables
date_time_format = "%I:%M %p %B %d"
room_users = dict()

def get_users_amount_by_chat():
    return {room: len(sids) for room, sids in room_users.items()}

@socketio.on('connect')
def on_connect():
    """Create connect log and call join-room event on client"""
        
    # Log connect message
    sid = request.sid
    user = session.get('name')
    print(f"{user} connected with sid: '{sid}'")
    
    # Call event on client for join room
    socketio.emit('join-room', to=sid)

@socketio.on('join-room')
def on_join(user_data: dict):
    """Save user sid in rooms"""
    
    # Parse data from client
    email: str = user_data.get('email')
    user: str = user_data.get('user')
    room: str = user_data.get('room')
    dpeartment: str = user_data.get('department')
    dpeartment_role: str = user_data.get('department_role')
    
    # Join the rooom by it's name and save log
    join_room(room)
    print(f"{user} joined room: '{room}'")
    
    # Count users in room
    if room not in room_users:
        room_users[room] = list()
        
    room_users[room].append(request.sid)
            
    # Send messages history to new user
    messages: tuple = get_messages(chat_name=room)
    
    if len(messages) > 0: # No history
        if isinstance(messages[0], bool):
            print(f"Error while retreiving chat history for chat: '{room}'")
        else:
            for message in messages:
                history = {
                    'name': message[0],
                    'msg': message[1],
                    'time': message[2].strftime(date_time_format).lstrip('0')
                }
                
                socketio.emit('receive-history', history, to=request.sid)
    
    # Send system message to room
    socketio.send(user + " has entered the chat", room=room)

@socketio.on('receive-message')
def on_message(user_data_and_message):
    
    # Parse data from client
    user_data_and_message = user_data_and_message.get('user_data')
    email: str = user_data_and_message.get('email')
    user: str = user_data_and_message.get('user')
    room: str = user_data_and_message.get('room')
    dpeartment: str = user_data_and_message.get('department')
    dpeartment_role: str = user_data_and_message.get('department_role')
    message: str = user_data_and_message.get('message')
                                            
    # Build message
    now: str = datetime.now().strftime(date_time_format).strip('0')
    message_data = {'name': user, 'msg': message, 'time': now}
        
    # Send message to room and save it to database
    socketio.emit('receive-message', message_data, to=room)
    add_message(user, room, message)
    
@socketio.on('leave-room')
def on_leave(user_data: dict):
    """Event triggered from client on leave-button click"""
        
    # Parse data from client
    user_data = user_data.get('user_data')
    email: str = user_data.get('email')
    user: str = user_data.get('user')
    room: str = user_data.get('room')
    dpeartment: str = user_data.get('department')
    dpeartment_role: str = user_data.get('department_role')
    
    # Leave room
    leave_room(room)
    
    # Remove sid from room
    if room in room_users and request.sid in room_users[room]:
        room_users[room].remove(request.sid)
        if len(room_users[room]) == 0:
            del room_users[room]
        
    # Call leave-room event on client side - redirect to '/rooms'
    socketio.emit('leave-room', {'url': '/rooms'}, to=request.sid)
        
    # Send system message to room and save log
    socketio.send(user + " has leaved the chat", room=room)
    print(f"{user} leaved room: '{room}'")
        
@socketio.on('disconnect')
def handle_disconnect():
    """Event triggered on reload, close page.
    When page is reloaded or closed - 'leave' event isn't triggered.
    """
    
    user = session.get('name')
    room = session.get('room')

    # Remove sid from room
    if room in room_users and request.sid in room_users[room]:
        room_users[room].remove(request.sid)
        if len(room_users[room]) == 0:
            del room_users[room]
    
    # Send system message and save log
    socketio.send(f"{user} has leaved the chat", room=room)
    print(user + " disconnected")