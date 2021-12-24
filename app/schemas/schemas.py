from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

class MessageBase(BaseModel):
    message: str
    author_user_id: int
    target_user_id: int

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
    email: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True