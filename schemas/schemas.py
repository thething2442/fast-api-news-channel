from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int
    author_id: int

class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    author_id: int

class Post(PostBase):
    id: int
    author_id: int
    comments: List[Comment] = []

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role: str = "user"

class User(UserBase):
    id: int
    role: str
    posts: List[Post] = []
    comments: List[Comment] = []

    model_config = ConfigDict(from_attributes=True)
