from sqlalchemy.orm import Session

from app.models.messages import Messages

def get_messages(db: Session):
    return db.query(Messages).all()

def get_messages_for_target(db: Session, target_user_id: str):
    return db.query(Messages).filter(Messages.target_user_id == target_user_id).filter(Messages.is_active == True).all()
