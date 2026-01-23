from pydantic import BaseModel, EmailStr
from typing import Literal

# Used when creating a user
class UserCreate(BaseModel):
    name: str
    email: EmailStr   # validate email properly
    password: str     # plain password input
    # role: str = "user"
    role: Literal["user", "admin"] = "user"  # default role is 'user'


class UserLogin(BaseModel):
    email: EmailStr
    password: str
        
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["user", "admin"]

    class Config:
        from_attributes = True
  # Enable ORM mode for compatibility with ORM objects
        # "It’s okay if the input is an ORM object — read its attributes just like a dict."