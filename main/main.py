from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models
from schemas.schemas import User, UserCreate, Post, PostCreate, Comment, CommentCreate
from database.database import Base , engine, SessionLocal, get_db
import os
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Lifespan handler started.")
    print(f"Attempting to create tables using DATABASE_URL: {os.getenv('DATABASE_URL')}")
    Base.metadata.create_all(bind=engine)
    print("Tables created (if they didn't exist).")
    yield

app = FastAPI(lifespan=lifespan_handler)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Dependency


@app.get('/')
def main():
    return {'Message':'Hello World'}
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/posts/", response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@app.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.post("/comments/", response_model=Comment)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)

@app.get("/comments/", response_model=List[Comment])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, skip=skip, limit=limit)
    return comments

@app.delete("/comments/{comment_id}", response_model=Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.delete_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment
