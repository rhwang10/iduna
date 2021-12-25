from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class MessageRules(Base):
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    tokens = Column(Integer, nullable=False)
    seconds = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    message = relationship("Messages", back_populates="rule")
