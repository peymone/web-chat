# Third party packages
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Text

# BuldIn packages
from datetime import datetime

# My modules
from .db import Base


class User(Base):
    """Users table model"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String, unique=True, index=True)
    chat_role = Column(String, default='user')
    department = Column(String, default=None)
    department_role = Column(String, default=None)
    registration_date = Column(DateTime, default=datetime.now())


class Chat(Base):
    """Chats table model"""

    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    password = Column(String, default=None)


class History(Base):
    """Chats history tabel model"""

    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    chat_id = Column(Integer, ForeignKey(Chat.id, ondelete='CASCADE'))
    message = Column(Text)
    date = Column(DateTime, default=datetime.now)

    user = relationship("User", backref="messages")