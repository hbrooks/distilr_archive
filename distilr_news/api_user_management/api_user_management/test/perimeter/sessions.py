from uuid import uuid4 
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from datetime import datetime
import json

from ..utilities import get_mock_redis
from ..template_utilities import get_mock_session
from ..template_utilities import get_mock_database_manager
from ..utilities import get_mock_cache_manager
from ... import create_app_helper
from ...exceptions.sessions import SessionNotFound

class SessionViews(TestCase):

    def test_GET_session_returns_200(self):
        
        session_id = str(uuid4())
        user_id = str(uuid4())
        created_at = datetime.now().timestamp()

        expected_sessions_contents = json.dumps({
            'userId': user_id,
            'createdAt': created_at,
        })

        mock_session = get_mock_session()
        mock_redis = get_mock_redis()
        mock_redis.get = MagicMock(return_value=expected_sessions_contents)
        mock_db_cm = get_mock_database_manager(mock_session)
        mock_cache_cm = get_mock_cache_manager(mock_redis)
        
        client = create_app_helper(
            database_connection_manager=mock_db_cm,
            cache_connection_manager=mock_cache_cm,
        ).test_client()
        r = client.get('/sessions/'+session_id)
        
        self.assertEqual(r.status_code, 200)
        response_body = r.json
        self.assertTrue('userId' in response_body)
        self.assertTrue('createdAt' in response_body)
        self.assertTrue(response_body['userId'] == user_id)
        self.assertTrue(response_body['createdAt'] == created_at)



    def test_GET_session_returns_404(self):

        mock_session = get_mock_session()
        mock_redis = get_mock_redis()
        mock_redis.get = MagicMock(return_value=None)
        mock_db_cm = get_mock_database_manager(mock_session)
        mock_cache_cm = get_mock_cache_manager(mock_redis)

        client = create_app_helper(
            database_connection_manager=mock_db_cm,
            cache_connection_manager=mock_cache_cm,
        ).test_client()
        r = client.get('/sessions/'+ str(uuid4()))

        self.assertEqual(r.status_code, 404)
        response_body = r.json
