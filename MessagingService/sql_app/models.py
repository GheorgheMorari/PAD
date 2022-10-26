from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, unique=False, index=True)
    receiver = Column(String, unique=False, index=True)
    timestamp = Column(DateTime, index=True)
    content = Column(String, unique=False, index=False)
