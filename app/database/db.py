# Third party packages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# BuldIn packages
from os import getenv
from os.path import exists


def configurate_db():
    """Configurate database and return engine"""

    # Set database url from env variable
    database_url = getenv('DATABASE')

    # Set default value if database url is None
    if database_url is None:
        database_url = 'app/database/chat.db'

    # Create engine and session objects
    engine = create_engine('sqlite:///' + database_url)
    Session = sessionmaker(engine)
    Base = declarative_base()

    return database_url, engine, Session, Base


# Set database configuration settings to Global
database_url, engine, Session, Base = configurate_db()


def create_db():
    """Create database if not exist"""

    if exists(database_url) is True:
        return False, "Database already exist"
    else:
        with Session() as session:
            Base.metadata.create_all(engine)
            return True, "Database successfully created"
