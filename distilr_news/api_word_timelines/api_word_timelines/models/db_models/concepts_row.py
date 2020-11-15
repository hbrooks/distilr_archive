from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from . import Base

class ConceptsRow(Base):

    __tablename__ = 'concepts'

    uri = Column(String(512), primary_key=True, nullable=False)
    type = Column(String(128), nullable=False)
    label = Column(String(128), nullable=False)
