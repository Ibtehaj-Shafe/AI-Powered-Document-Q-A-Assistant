from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Backend.database.database import get_db
from Backend.models import User
from Backend.dependencies.jwt import decode_token
from jose import JWTError 

# used to implement OAuth2 password flow authentication using a Bearer token scheme
# The tokenUrl specifies where the client sends credentials to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")   # #Declare Bearer Token Authentication

# ___________________Authenticating_________________________
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        user = db.query(User).get(int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ___________________Authorization_________________________
def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )
    return current_user

    # ___________________General User Dependency_________________________
def require_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces authentication and returns the current user.
    Use this in endpoints where any authenticated user is allowed.
    """
    return current_user

