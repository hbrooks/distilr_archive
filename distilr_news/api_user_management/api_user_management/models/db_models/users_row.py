from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime


from . import Base

class UsersRow(Base):

    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True)
    email = Column(String(1024), nullable=True)
    password = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False)
    type = Column(String(128), nullable=False)
    address = Column(String(128), nullable=True)

