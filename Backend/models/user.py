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

    
# - UserStats because each user should have only one stats record (one‑to‑one relationship).
# - uselist tells This relationship should be treated as a scalar (single object), not a list

# stats = relationship("UserStats", back_populates="user", uselist=False)
# documents = relationship("Document", back_populates="user")

"""
- Purpose: It tells Pydantic that when you create a response model from an ORM object (like a SQLAlchemy model), it should read the object’s attributes instead of expecting a plain dictionary.
- Without it, if you try to return a SQLAlchemy object directly from your FastAPI route, Pydantic would complain because it expects a dict.
- With it, Pydantic knows: “Okay, this is an ORM object, I will grab its attributes (user.id, user.email, etc.) and build the response.”
"""