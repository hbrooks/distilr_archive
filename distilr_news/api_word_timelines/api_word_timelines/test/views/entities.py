from uuid import uuid4 
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import MagicMock
from datetime import datetime
import json

from ..template_utilities import get_mock_session
from ..template_utilities import get_mock_database_manager
from ... import create_app_helper

class EntityViews(TestCase):

    def test_get_entity(self):

        entity_one_id = str(uuid4())

        entity_one = Mock()
        entity_one.to_external_dict = Mock(return_value={'id':entity_one_id})
        timeline_one = Mock()

        mock_session = get_mock_session()
        mock_db_cm = get_mock_database_manager(mock_session=mock_session)

        mock_entity_manager = Mock()
        mock_entity_manager.get_by_id = Mock(return_value=entity_one)
        mock_ibm_watson_api = Mock()

        mock_timeline_manager = Mock(
            mock_entity_manager,
            mock_ibm_watson_api,
            is_allowed_to_create_new=False,
            is_allowed_to_get_articles=False)
        mock_timeline_manager.get_latest_timeline = Mock(return_value=timeline_one)

        client = create_app_helper(
            mock_db_cm,
            mock_entity_manager, 
            mock_timeline_manager, 
        ).test_client()
        r = client.get('/entities/'+entity_one_id)
        
        self.assertEqual(r.status_code, 200)
        response_body = r.json
