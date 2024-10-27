# Third party packages
from flask import request, session, render_template, redirect, url_for, flash

# My modules
from . import chat_bp
from .validations import RoomForm
from ..database import get_chats
from .events import get_users_amount_by_chat


@chat_bp.route('/chat')
@chat_bp.route('/')
def chat():
    """Chat for specific room"""

    # Get data from session
    email = session.get('email', '')
    user = session.get('name', '')
    room = session.get('room', '')
    department = session.get('department', '')
    department_role = session.get('department_role', '')

    # User not authorized and not picked room
    if user == '' or room == '':
        return redirect(url_for('chat.rooms'))
    else:        
        # return render_template('chat.html', room=room, email=email, user=user, department=department, department_role=department_role)
        return render_template('chat.html', room=room, email=email, user=user, department=department, department_role=department_role)


@chat_bp.route('/rooms', methods=['GET', 'POST'])
def rooms():
    """Room list and description, input chat form"""

    # Remove room name from session
    try:
        del session['room']
    except KeyError:
        pass
    
    # Form object for validations check
    form = RoomForm(request.form)

    # Get all chat rooms from database
    chats = get_chats()

    # get amount of users in each room
    room_users = get_users_amount_by_chat()
    
    # User is not passed registration or authorization - full name not in session
    if (request.method == 'GET') and (session.get('name') is None):
        return redirect(url_for('auth.login'))

    # User is passed registration or authorization - full name in session
    elif (request.method == 'GET') and (session.get('name') is not None):
        return render_template('rooms.html', form=form, rooms=chats, users=room_users)

    # User enter form - check validation
    elif request.method == 'POST' and form.validate():

        # Check if picked chat room exist in database
        picked_chat = [chat for chat in chats if chat.id == form.room.data]
        if len(picked_chat) == 0:  # Chat ID not in database

            flash(f"Room with ID {form.room.data} does not exist")
            return render_template('rooms.html', form=form, rooms=chats, users=room_users)

        else:  # Chat ID in database

            # Parse data from database
            room_name: str = picked_chat[0].name
            password: str | None = picked_chat[0].password

            # Check password identity
            if password is None or password == form.password.data:
                session['room'] = room_name
                return redirect(url_for('chat.chat'))
            else:
                flash("Incorrect password for room")
                return render_template('rooms.html', form=form, rooms=chats, users=room_users)
