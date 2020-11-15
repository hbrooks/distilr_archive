from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime


from . import Base

class UserEventsRow(Base):

    __tablename__ = 'user_events'
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False)
    event_type = Column(String(128), nullable=False)
    occured_at= Column(DateTime, nullable=False)


    def to_external_dict(self):
        return {
            'userId': self.user_id,
            'type': self.event_type,
        }