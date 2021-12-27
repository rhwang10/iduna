from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

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

class UserBase(BaseModel):
    name: str
    display_name: str

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
