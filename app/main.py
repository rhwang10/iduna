import json
import sqlalchemy

from fastapi import FastAPI, APIRouter, Depends
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from typing import List

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine

from app.cache.user_cache import UserCache

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
user_cache = UserCache(SessionLocal())

@app.get("/messages/{user_id}", response_model=schemas.Message)
async def getMessageForUser(user_id, db: Session = Depends(get_db), redis = Depends(get_redis)):
    msgs = get_messages_for_target(db, user_id)

    for candidate in redis.rankMessages(user_id, msgs):
        can_send = redis.checkMessage(user_id, candidate)

        if can_send:
            return candidate

    # If no message, return an empty response
    return Response(json.dumps({}), status_code=HTTP_200_OK)

@app.get("/messages", response_model=List[schemas.Message])
async def getMessages(db: Session = Depends(get_db)):
    msgs = get_messages(db)
    return msgs

@app.get("/users", response_model=schemas.CachedUser)
async def getUserByTag(name: str, id: str):
    tag = f"{name}#{id}"
    try:
        user = user_cache[tag]
    except sqlalchemy.exc.NoResultFound as e:
        print(f"No user found for name {name} and id {id}")
        return Response(json.dumps({}), status_code=HTTP_404_NOT_FOUND)
    return user
