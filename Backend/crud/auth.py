from Backend.models.user import User
from Backend.dependencies.jwt import create_access_token, decode_token, create_refresh_token
from fastapi import HTTPException
from sqlalchemy.orm import Session
from Backend.dependencies.password import verify_password



def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    return {
        "access_token": create_access_token(user.id, user.role),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


def refresh_access_token(db: Session, refresh_token: str) -> dict:
    # Decode and validate refresh token
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Get user from DB
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Issue new access token
    new_access_token = create_access_token(user.id, user.role)

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,  # keep same refresh token (no rotation here)
        "token_type": "bearer",
    }
