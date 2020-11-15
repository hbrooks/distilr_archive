from uuid import uuid4 
from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime
import json

from sqlalchemy.orm import Session

from ..models import DatabaseConnectionManager


def get_mock_session():
    mock_session = Session()
    mock_session.add = MagicMock()
    return mock_session

def get_mock_database_manager(mock_session=None):

    if mock_session == None:
        mock_session = get_mock_session()

    connection_details = {}
    connection_details['POSTGRES_USER'] = None
    connection_details['POSTGRES_PASSWORD'] = None
    connection_details['POSTGRES_HOST_NAME'] = None
    connection_details['POSTGRES_HOST_PORT'] = 1000
    connection_details['POSTGRES_DB'] = None

    mock_db_cm = DatabaseConnectionManager(connection_details)
    mock_db_cm.get_session = MagicMock(return_value=mock_session)

    return mock_db_cm

