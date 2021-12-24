import json

from fastapi import FastAPI, APIRouter, Depends
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from typing import List

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine

from app.redis.client import RedisClient

import app.schemas.schemas as schemas

from app.sql.messages import (
    get_messages,
    get_messages_for_target
)

def get_redis():
    redis = RedisClient()
    yield redis

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# todo: set up latency monitoring w/ middlewares https://fastapi.tiangolo.com/tutorial/middleware/

app = FastAPI()
router = APIRouter()

@app.get("/messages/{user_id}", response_model=schemas.Message)
async def getMessageForUser(user_id, db: Session = Depends(get_db), redis = Depends(get_redis)):
    msgs = get_messages_for_target(db, user_id)

    for candidate in msgs:
        key = RedisClient.key(user_id, candidate.id)

        if not redis.exists(key):
            redis.set(key, 5)
            return candidate

    # If no message, return an empty response
    return Response(json.dumps({}), status_code=HTTP_200_OK)

@app.get("/messages", response_model=List[schemas.Message])
async def getMessages(db: Session = Depends(get_db)):
    msgs = get_messages(db)
    return msgs
