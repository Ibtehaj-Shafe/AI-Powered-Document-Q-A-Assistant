from pydantic import BaseModel, EmailStr
from datetime import datetime

class OTPResetCreate(BaseModel):
    email: EmailStr
    # otp: str

class OTPResetRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class OTPResetResponse(BaseModel):
    id: int
    email: EmailStr
    expires_at: datetime
    used: bool

    class Config:
        from_attributes = True


