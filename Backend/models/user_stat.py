# Backend/models/user_stats.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Backend.database.database import Base

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    files_uploaded_count = Column(Integer, default=0)
    questions_asked_count = Column(Integer, default=0)

    # Relationship back to User
    user = relationship("User", back_populates="stats")