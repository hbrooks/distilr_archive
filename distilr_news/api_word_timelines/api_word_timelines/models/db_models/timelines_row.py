from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from . import Base

class TimelinesRow(Base):

    __tablename__ = 'timelines'

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, nullable=False)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)
    concept_uri = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
