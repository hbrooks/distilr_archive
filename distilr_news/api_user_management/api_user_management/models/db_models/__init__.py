import sys
import os

from ..database_connection_manager import DatabaseConnectionManager

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# # for creating foreign key relationship between the tables
# from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()

from .user_events_row import UserEventsRow
from .users_row import UsersRow

engine = create_engine(DatabaseConnectionManager.get_connection_string('root', 'flamingo', 'mysql_relational_database', '3306', 'distilr_news'))
Base.metadata.create_all(engine)
