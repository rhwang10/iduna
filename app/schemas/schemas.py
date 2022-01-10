from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

################################
# MessageRule
################################

class MessageRuleBase(BaseModel):
    message_id: int
    tokens: int
    seconds: int

class MessageRuleCreate(MessageRuleBase):
    pass

class MessageRule(MessageRuleBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

################################
# Message
################################


class MessageBase(BaseModel):
    message: str
    author_user_id: int
    target_user_id: int
    rule: MessageRule

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    is_active: bool
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

################################
# User
################################

class UserBase(BaseModel):
    name: str
    display_name: str
    discord_id: int

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    email: str
    created_at: datetime
    modified_at: datetime

class CachedUser(UserBase):
    id: int

    class Config:
        orm_mode = True

################################
# Track
################################

class TrackEvent(BaseModel):
    id: str
    requested_by: str
    event_type: str
    title: str
    description: str
    webpage_url: str
    duration: int
    timestamp: datetime
    guild_id: str
