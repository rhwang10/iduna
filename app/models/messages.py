from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.db.base_class import Base

class Messages(Base):
    id = Column(Integer, primary_key=True, index=True)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(256), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
