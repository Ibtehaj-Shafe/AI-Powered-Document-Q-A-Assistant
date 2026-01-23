from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean,DateTime
from Backend.database.database import Base

class OTPReset(Base):
    __tablename__ = "otp_reset"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    otp_hash = Column(Text, nullable=False)
    # expires_at = Column(TIMESTAMP, nullable=False)
    # expires_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)