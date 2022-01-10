from sqlalchemy.orm import Session

from app.models.users import Users

def get_user_by_discord_id(db: Session, discord_id: int):
    return db.query(Users).filter(Users.discord_id == discord_id).one()
