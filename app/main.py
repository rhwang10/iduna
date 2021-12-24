from fastapi import FastAPI, APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine

import app.schemas.schemas as schemas

from app.sql.messages import (
    get_messages,
    get_messages_for_target
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# todo: set up latency monitoring w/ middlewares https://fastapi.tiangolo.com/tutorial/middleware/

app = FastAPI()
router = APIRouter()

@app.get("/messages/{user_id}", response_model=List[schemas.Message])
async def getMessageForUser(user_id, db: Session = Depends(get_db)):
    return get_messages_for_target(db, user_id)

@app.get("/messages", response_model=List[schemas.Message])
async def getMessages(db: Session = Depends(get_db)):
    msgs = get_messages(db)
    return msgs
