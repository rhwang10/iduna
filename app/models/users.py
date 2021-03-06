from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)
    discord_id = Column(Integer, nullable=True, unique=True)
    display_name = Column(String(256), nullable=False)
    email = Column(String(256))
    hashed_password = Column(String(256))
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
