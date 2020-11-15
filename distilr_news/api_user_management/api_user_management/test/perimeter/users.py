from uuid import uuid4 
from unittest import TestCase
from unittest.mock import MagicMock
# from unittest.mock import patch
from datetime import datetime
import json

from sqlalchemy.orm import Session
from redis import Redis

from ..utilities import get_mock_redis
from ..template_utilities import get_mock_session
from ..template_utilities import get_mock_database_manager
from ..utilities import get_mock_cache_manager
from ... import create_app_helper
from ...models import DatabaseConnectionManager
from ...models import CacheConnectionManager
from ...models import EventManager


class UsersViews(TestCase):

    def test_POST_users_returns_200(self):

        email = str(uuid4()).replace('-', '')+"@gmail.com"
        password = str(uuid4()).replace('-', '')
        request_body = {
            'email': email,
            'password': password
        }

        mock_session = get_mock_session()
        mock_db_cm = get_mock_database_manager(mock_session=mock_session)
        mock_cache_cm = get_mock_cache_manager()
    
        client = create_app_helper(
            database_connection_manager=mock_db_cm,
            cache_connection_manager=mock_cache_cm,
        ).test_client()
        r = client.post('/users', data=json.dumps(request_body), headers={"content-type":"application/json"})
        
        self.assertEqual(r.status_code, 200)
        response_body = r.json
        self.assertTrue('userId' in response_body)
