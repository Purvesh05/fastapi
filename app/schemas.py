from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class User(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True  # orm_mode has been replcaed to from_attributes

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at: datetime
    user_id: int
    owner: User 
    class Config:
        from_attributes = True  # orm_mode has been replcaed to from_attributes

class PostVote(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True  # orm_mode has been replcaed to from_attributes


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)