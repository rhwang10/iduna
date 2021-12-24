from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base

class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)
    display_name = Column(String(256), nullable=False)
    email = Column(String(256))
    hashed_password = Column(String(256))
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
