from sqlalchemy.orm import Session

from app.models.messages import Messages
from app.models.message_rules import MessageRules
from app.schemas.schemas import MessageCreate

def get_messages(db: Session):
    return db.query(Messages).all()

def get_messages_for_target(db: Session, target_user_id: str):
    return db.query(Messages) \
            .filter(Messages.target_user_id == target_user_id) \
            .filter(Messages.is_active == True) \
            .all()

def create_message(db: Session, message: MessageCreate):
    db_msg = Messages(
        author_user_id=message.author_user_id,
        target_user_id=message.target_user_id,
        message=message.message,
        is_active=message.is_active
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    id = db_msg.id

    db_msg_rule = MessageRules(
        message_id=id,
        tokens=message.rule.tokens,
        seconds=message.rule.seconds
    )

    db.add(db_msg_rule)
    db.commit()
    db.refresh(db_msg_rule)

    msg_rule_id = db_msg_rule.id

    return (id, msg_rule_id)
