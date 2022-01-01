from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class TrackEvents(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    youtube_id = Column(String(256), primary_key=True, index=True)
    requested_by = Column(String(256), nullable=False, index=True)
    event_type = Column(String(256), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    guild_id = Column(String(256), nullable=False)
    title = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)
    duration = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
