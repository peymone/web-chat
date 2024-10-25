# Third party packages
from flask_socketio import join_room, leave_room, send, emit
from flask import session, request

from datetime import datetime

# My modules
from .. import socketio
from ..database import add_message, get_chats, get_messages


# Configuration variables
date_time_format = "%I:%M %p %B %d"
chats_from_db = get_chats()
rooms_with_sid = dict()


def get_users_amount_per_chat() -> dict:
    """Get amount of users in each chat"""
    
    return {chat: len(sids) for chat, sids in rooms_with_sid.items()}

@socketio.on('connect')
def on_connect(auth):
    """Create connect log and call join room event on client"""
    
    # Log connect message
    sid = request.sid
    user = auth.get('user')
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
    
    # Create room and add sid
    rooms_with_sid[room] = list()
    rooms_with_sid[room].append(request.sid)
    
    # Join the rooom by it's name
    join_room(room)
    print(f"{user} joined room: '{room}'")
    
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
                
                emit('receive-history', history, to=request.sid)
    
    # Send message to room
    if request.sid in rooms_with_sid[room]:
        message = user + " has entered the chat"    
        socketio.send(message, room=room)

@socketio.on('server-message')
def on_message(user_data_and_message):
    
    # Parse data from client
    email: str = user_data_and_message.get('email')
    user: str = user_data_and_message.get('user')
    room: str = user_data_and_message.get('room')
    dpeartment: str = user_data_and_message.get('department')
    dpeartment_role: str = user_data_and_message.get('department_role')
    message: str = user_data_and_message.get('message')
    
    # Broadcast message to chat room
    if request.sid in rooms_with_sid[room]:
        # Build message
        now: str = datetime.now().strftime(date_time_format).strip('0')
        message_data = {'name': user, 'msg': message, 'time': now}
        
        # Send message and save it to database
        socketio.emit('client-message', message_data, to=room)
        add_message(user, room, message)
    
@socketio.on('leave-room')
def on_leave(user_data: dict):
    
    # Parse data from client
    email: str = user_data.get('email')
    user: str = user_data.get('user')
    room: str = user_data.get('room')
    dpeartment: str = user_data.get('department')
    dpeartment_role: str = user_data.get('department_role')
    
    # Delete user sid from rooms and leave room
    if request.sid in rooms_with_sid[room]:
        rooms_with_sid[room].remove(request.sid)
        leave_room(room)
        
        # Call event on client side to clear session and redirect
        emit('leave-room', {'url': '/rooms'}, to=request.sid)
    
socketio.on('disconnect')
def on_disconnect():
    """I don't know when this invoke. Just remove sid from rooms"""
    
    for room, sids in rooms_with_sid.items():
        if request.sid in sids:
            sids.remove(request.sid)
            leave_room(room)
    
    name = session.get('name')
    print(name + " disconnected")