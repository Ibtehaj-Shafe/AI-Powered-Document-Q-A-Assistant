from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Backend.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique= True, nullable=False)
    role = Column(String, nullable=False, default="user")  # only "admin" or "user"
    hashed_password = Column(String, nullable=False)

    documents = relationship("Document", back_populates="user") #one-to-many (A user can upload many documents)
    stats = relationship("UserStats", back_populates="user", uselist=False) #one-to-one (A user has one stats record)

    
# - uselist tells This relationship should be treated as a scalar (single object), not a list

"""
- By default, SQLAlchemy assumes a one-to-many relationship when you declare relationship("SomeModel").
- That means it expects the attribute (stats in your case) to be a list-like collection of related objects.

"""
