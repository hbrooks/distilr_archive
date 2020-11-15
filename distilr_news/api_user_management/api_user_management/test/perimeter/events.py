# from uuid import uuid4 
# from unittest import TestCase
# from unittest.mock import MagicMock
# # from unittest.mock import patch
# from datetime import datetime
# import json

# from sqlalchemy.orm import Session
# from redis import Redis

# from ..utilities import get_mock_redis
# from ..template_utilities import get_mock_session
# from ..template_utilities import get_mock_database_manager
# from ..utilities import get_mock_cache_manager
# from ... import create_app_helper


# class EventsView(TestCase):

#     def test_POST_events_returns_200(self):

#         user_id = str(uuid4())
#         event_type = "test event type"
#         occured_at = datetime.now().timestamp()
#         request_body = {
#             'userId': user_id,
#             'eventType': event_type,
#             'occuredAt': occured_at,
#         }

#         mock_session = get_mock_session()
#         mock_db_cm = get_mock_database_manager(mock_session=mock_session)
#         mock_cache_cm = get_mock_cache_manager()
    
#         client = create_app_helper(
#             database_connection_manager=mock_db_cm,
#             cache_connection_manager=mock_cache_cm,
#         ).test_client()
#         r = client.post('/events', data=json.dumps(request_body), headers={"content-type":"application/json"})
        
#         self.assertEqual(r.status_code, 200)
