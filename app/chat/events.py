# Third party packages
from flask_socketio import join_room, leave_room, send, emit
from flask import session

from datetime import datetime

# My modules
from .. import socketio
from ..database import add_message, get_chats, get_messages


# Configuration variables
CONNECTION_MSG = 'CONNECTION_MSG'
chats = get_chats()  # Get chats from database
users_in_room = {chat.name: [] for chat in chats}  # Dict for users saving
date_time_format = "%I:%M %p %B %d  "  # time format for messages


def get_users_amount_per_chat() -> dict:
    """Get amount of users in each chat"""

    return {chat: len(users) for chat, users in users_in_room.items()}

@socketio.on('join')
def on_join(data):
    """Event for chat joining"""

    # Get data from client's session
    user_name = session.get('name')
    room_name = session.get('room')

    # Get message history from database by room name
    messages: tuple = get_messages(chat_name=room_name)

    # Send messages history to client
    if len(messages):  # No messages in chat
        if isinstance(messages[0], bool):  # Error occured
            on_disconnect()
        else:
            for message in messages:
                if user_name in users_in_room[room_name]:  # User currently in room
                    pass
                else:
                    emit('rcv-history', {
                        'name': message[0], 'msg': message[1], 'time': message[2].strftime(date_time_format).lstrip('0')})

    # Join the room
    join_room(room_name)
    users_in_room[room_name].append(user_name)

    # For logging
    print(user_name + ' joined room ' + room_name)

    # Broadcast join message to chat room
    send(user_name + ' has entered the chat', room=room_name)


@socketio.on('leave')
def on_leave(data):
    """Event for chat leaving"""

    # Get data from client's session
    user_name = session.get('name')
    room_name = session.get('room')

    print(user_name + ' leaved room ' + room_name)  # For logging

    # Check if user currently in room
    if user_name in users_in_room[room_name]:

        # Remove user from room
        leave_room(room_name)
        users_in_room[room_name].remove(user_name)

        # Send redirect command to client
        emit('leave-redirect', {'url': '/rooms'})

    # Broadcast leave message to chat room
    send(user_name + ' has leaved the chat', room=room_name)


@socketio.on('disconnect')
def on_disconnect():
    """Del user from chat on disconnect evenv - reload, etc."""

    # Get data from client's session
    user_name = session.get('name')
    room_name = session.get('room')

    print(user_name + ' has been disconnected')  # For logging

    # Check if user currently in room
    if user_name in users_in_room[room_name]:

        # Remove user from room
        leave_room(room_name)
        users_in_room[room_name].remove(user_name)


@socketio.on('message')
def handle_message(data):
    """Receive message from client"""

    # Get data from client's session
    user_name = session.get('name')
    room_name = session.get('room')

    # Get message from client
    message = data.get('msg')

    # handle connection message
    if message == CONNECTION_MSG:
        print(user_name + " connected")
        socketio.emit('join_room')

    # Handle common messages
    else:
        now = datetime.now().strftime(date_time_format).strip('0')
        message_data = {'name': user_name, 'msg': message, 'time': now}
        emit('recieve-msg', message_data, room=room_name)

        # Save message to database
        add_message(user_name, room_name, message)
