from datetime import datetime
from uuid import uuid4
import json

from redis import Redis

from ..exceptions.sessions import SessionNotFound
from .event_manager import EventManager


class SessionManager:

    SESSION_DURATION_SECONDS = 60*60

    def __init__(self, connection_manager, _):
        self.connection_manager = connection_manager
        self.connection_manager.validate_connection() # TODO: May not always want this.
        self.cache = connection_manager.get_connection()

    def create(self, session, user, creation_timestamp):
        EventManager._create_generic_event(session, user.id, EventManager.SESSION_CREATED_EVENT_TYPE, creation_timestamp)
        session_id = self._create(user, creation_timestamp)
        return session_id

    def _create(self, user, creation_timestamp):
        session_key = ':'.join([
            'session',
            user.id
        ])
        session_value = {
            'userId': user.id,
            'createdAt': creation_timestamp,
            # TODO: Add events for this session.
        }
        self.cache.set(
            session_key,
            json.dumps(session_value)
        )
        return session_key


    def get(self, session_key, as_of):
        session_contents = self.cache.get(session_key)
        if session_contents == None:
            raise SessionNotFound(session_key, as_of)
        else:
            session_contents = json.loads(session_contents)
        
        if session_contents['createdAt'] + SessionManager.SESSION_DURATION_SECONDS < as_of:
            raise SessionNotFound(session_key, as_of)
        
        return session_contents

