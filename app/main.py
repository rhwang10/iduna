import json
import sqlalchemy
from typing import List

# FastAPI and starlette
from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from sse_starlette.sse import EventSourceResponse

# SQLAlchemy
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine

# App imports
from app.cache.user_cache import UserCache
from app.redis.client import RedisClient
import app.schemas.schemas as schemas
from app.sql.messages import (
    get_messages,
    get_messages_for_target
)
from app.sql.track_events import (
    insertTrackEvent
)
from app.utils.auth import VerifyToken
from app.utils.constants import REDIS_SS_DELIMITER

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
token_auth_scheme = HTTPBearer()
user_cache = UserCache(SessionLocal())

@app.get("/messages/{user_id}", response_model=schemas.Message)
async def getMessageForUser(user_id: str,
                            token: str = Depends(token_auth_scheme),
                            db: Session = Depends(get_db),
                            redis = Depends(get_redis)):
    authResult = VerifyToken(token.credentials).verify()

    if authResult.get("error"):
        return Response(json.dumps(authResult), status_code=HTTP_400_BAD_REQUEST)

    msgs = get_messages_for_target(db, user_id)

    for candidate in redis.rankMessages(user_id, msgs):
        can_send = redis.checkMessage(user_id, candidate)

        if can_send:
            return candidate

    # If no message, return an empty response
    return Response(json.dumps({}), status_code=HTTP_200_OK)

@app.get("/messages", response_model=List[schemas.Message])
async def getMessages(token: str = Depends(token_auth_scheme),
                      db: Session = Depends(get_db)):

    authResult = VerifyToken(token.credentials).verify()

    if authResult.get("error"):
        return Response(json.dumps(authResult), status_code=HTTP_400_BAD_REQUEST)

    msgs = get_messages(db)
    return msgs

@app.get("/users", response_model=schemas.CachedUser)
async def getUserByTag(discord_id: int,
                       token: str = Depends(token_auth_scheme)):
    authResult = VerifyToken(token.credentials).verify()
    if authResult.get("error"):
        return Response(json.dumps(authResult), status_code=HTTP_400_BAD_REQUEST)

    try:
        user = user_cache[discord_id]
    except sqlalchemy.exc.NoResultFound as e:
        print(f"No user found for Discord Id: {discord_id}")
        return Response(json.dumps({}), status_code=HTTP_404_NOT_FOUND)
    return user

@app.get("/toptracks/{guild_id}")
async def getTopTracks(guild_id: str,
                       limit: int,
                       token: str = Depends(token_auth_scheme),
                       redis = Depends(get_redis)):
    authResult = VerifyToken(token.credentials).verify()
    if authResult.get("error"):
        return Response(json.dumps(authResult), status_code=HTTP_400_BAD_REQUEST)

    topTracks = redis.getNTopTracks(guild_id, limit)

    resp = {}
    for memberName, timesPlayed in topTracks:
        _, title = memberName.split(REDIS_SS_DELIMITER)
        resp[title] = int(timesPlayed)

    return Response(json.dumps(resp, ensure_ascii=False))

@app.post("/trackevents")
async def events(track_event: schemas.TrackEvent,
                 token: str = Depends(token_auth_scheme),
                 db: Session = Depends(get_db),
                 redis = Depends(get_redis)):

    authResult = VerifyToken(token.credentials).verify()
    if authResult.get("error"):
        return Response(json.dumps(authResult), status_code=HTTP_400_BAD_REQUEST)
    # Insert a row into track_events table, and update the sorted set
    # TODO: exception handling
    # TODO: if not seen before, index it into elasticsearch
    insertTrackEvent(db, track_event)
    redis.updateTrackRank(track_event)
    return Response(json.dumps({}), status_code=HTTP_200_OK)
