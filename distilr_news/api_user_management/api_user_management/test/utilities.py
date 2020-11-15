from uuid import uuid4 
from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime
import json

from sqlalchemy.orm import Session
from redis import Redis

from ..models import CacheConnectionManager
from ..models import EventManager


def get_mock_redis():
    return Redis() # NOTE: This might break... It's actually building a real connection, right?


def get_mock_cache_manager(mock_redis=None):

    if mock_redis == None:
        mock_redis = get_mock_redis()

    connection_details = {}
    connection_details['host_name'] = ''
    connection_details['port'] = 100
    mock_cache_cm = CacheConnectionManager(connection_details)
    mock_cache_cm.validate_connection = MagicMock()
    mock_cache_cm.get_connection = MagicMock(return_value=mock_redis)

    return mock_cache_cm