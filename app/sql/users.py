from sqlalchemy.orm import Session

from app.models.users import Users

def get_user_by_tag(db: Session, tag: str):
    print(tag)
    return db.query(Users).filter(Users.display_name == tag).one()
