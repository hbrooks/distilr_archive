from datetime import datetime
from uuid import uuid4

from .db_models import UserEventsRow
from .user_event import UserEvent

class EventManager:

    # Event Types:
    ACCOUNT_CREATION_EVENT_TYPE = 'account_creation'
    TIMELINE_REQUESTED_EVENT_TYPE = 'timeline_requested'

    def __init__(self):
        pass

    def create_user(self, session, user, occured_at):
        return self.create_generic_event(
            session,
            user.id,
            EventManager.ACCOUNT_CREATION_EVENT_TYPE,
            occured_at,
        )

    def get_all(self, session, user_id):
        rows = session.query(UserEventsRow).filter(UserEventsRow.user_id == user_id).all()
        return [self.build_user_event_from_row(r) for r in rows]

    def build_user_event_from_row(self, row):
        return UserEvent(
            row.id,
            row.user_id,
            row.event_type,
            row.occured_at
        )

    def create_generic_event(self, session, user_id, event_type, occured_at):
        new_user_event = UserEventsRow(
            id=str(uuid4()),
            user_id=user_id,
            event_type=event_type,
            occured_at=occured_at,
        )
        session.add(new_user_event)
        return self.build_user_event_from_row(new_user_event)
