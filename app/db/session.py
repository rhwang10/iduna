import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# Workaround to allow dyanmic URI to work w/ Heroku
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI= SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
