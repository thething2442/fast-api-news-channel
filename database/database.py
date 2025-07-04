# database/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in your .env file.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db_and_tables():
    print("Attempting to create database tables...")
    try:
        # Base.metadata.create_all(bind=engine) inspects all models that inherit from Base
        # and creates corresponding tables in the database if they don't already exist.
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully (or already existed).")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Consider logging this error more formally in a production environment.
from models.models import User, Post, Comment # <-- UNCOMMENT/ADD THIS LINE
# --- Dependency to get a database session ---
# This function is used by FastAPI's Depends() to provide a database session to your routes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()