"""
consist of 
engine
session
Base
get_db FASTAPI dependency
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Backend.config import base_url

Engine = create_engine(base_url)#connnects to db
session_local = sessionmaker(bind=Engine)#Handles db operations
Base = declarative_base() #Registry of ORM models

#Dependency of FASTAPI

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()    