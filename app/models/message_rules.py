from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class MessageRules(Base):
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    tokens = Column(Integer, nullable=False)
    seconds = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    message = relationship("Messages", back_populates="rule")
