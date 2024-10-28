# Third party packages
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# My modules
from .db import Session
from .models import User, Chat, History


def add_user(email: str, hashed_password: str, full_name: str, department: str, department_role: str):
    """Add new user to database"""

    # Create user object
    new_user = User(email=email, password=hashed_password, full_name=full_name,
                    department=department, department_role=department_role)

    # Add user to database
    with Session() as session:
        try:
            session.add(new_user)
            session.commit()
            return True, "New user successfully added to database"

        except IntegrityError as error:
            session.rollback()
            return False, "User already in database"

        except Exception as error:
            session.rollback()
            return False, "Transaction error while adding new user to database"


def add_chat(name: str, description: str, password: str = None):
    """Add new chat room to database""" 

    # Create chat object
    new_chat = Chat(name=name, description=description, password=password)

    # Add chat to database
    with Session() as session:
        try:
            session.add(new_chat)
            session.commit()
            return True, "New chat successfully added to database"

        except IntegrityError:
            session.rollback()
            return False, f"Chat '{name}' already exist"

        except Exception:
            session.rollback()
            return False, "Transaction error while adding new chat to database"


def add_message(user_name: str, chat_name: str, message: str):
    """Add new message to database"""

    # Get user and chat objects for id
    user = get_user_by_name(user_name)[0]
    chat = get_chats(chat_name)[0]

    # Create message history object
    new_message = History(user_id=user.id, chat_id=chat.id, message=message)

    # Add message to database
    with Session() as session:
        try:
            session.add(new_message)
            session.commit()
            return True, "New message successfully added to database"
        except Exception:
            return "Transaction error while adding new message to database"


def get_user_by_name(name: str):
    """Get user data from database by it's name"""

    with Session() as session:
        try:
            user = session.scalars(select(User).where(User.full_name == name))
            return user.all()
        except Exception:
            return None, "Transaction error while getting user from database"


def get_user_by_email(email: str):
    """Get user data from database by it's email"""

    with Session() as session:
        try:
            user = session.scalars(select(User).where(User.email == email))
            return user.all()
        except Exception:
            return None, "Transaction error while getting user from database"


def get_chats(chat_name: str = None):
    """Get chats from database by specific name or all"""

    with Session() as session:
        try:
            if chat_name is None:
                chats = session.scalars(select(Chat))
            else:
                chats = session.scalars(select(Chat).where(Chat.name == chat_name))

            return chats.all()

        except Exception:
            return None, "Transaction error while getting chats from database"


def get_messages(chat_name: str, limit:int = None):
    with Session() as session:
        try:
            # Get chat id by it's name
            chat = get_chats(chat_name)
            if chat[0] is None:
                return None, "Transaction error while getting message history from database"
            else:
                if limit is None: # Return all history from specific chat
                
                    # Retrieve all messages from specific chat
                    chat_id = chat[0].id
                    history = session.scalars(select(History).where(History.chat_id == chat_id).order_by(History.date))
                    messages = [(msg.user.full_name, msg.user.department, msg.user.department_role, msg.message, msg.date)  for msg in history.all()]
    
                else: # Return history with limit
                    
                    chat_id = chat[0].id
                    history = session.query(History).where(History.chat_id == chat_id).limit(limit)                    
                    messages = [(msg.user.full_name, msg.message, msg.date)  for msg in history.all()]
                    
                return messages
            
        except Exception:
            return None, "Transaction error while getting message history from database"
