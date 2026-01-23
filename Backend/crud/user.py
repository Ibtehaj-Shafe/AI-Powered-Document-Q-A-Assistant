from sqlalchemy.orm import Session
from Backend.models import User
from Backend.models import UserStats
from Backend.dependencies.password import hash_password
from Backend.crud.otp import verify_otp
from fastapi import HTTPException

def create_user(user, db: Session):
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),  # match model column name
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(User).all()


def reset_password(db: Session, email: str, otp: str, new_password: str):
    # 1. Verify OTP
    try:
        verify_otp(db, email, otp)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Hash and update password
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password reset successful"}


# def reset_password(db: Session, email: str, otp: str, new_password: str):
#     verify_otp(db, email, otp)
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise ValueError("Invalid request")
#     user.hashed_password = hash_password(new_password)
#     db.commit()
#     return {"message": "Password reset successful"}


# def login_user(user: UserLogin, db: Session):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user:
#         return {"error": "Invalid email or password"}
#     if not verify_password(user.password, db_user.hashed_password):
#         return {"error": "Invalid email or password"}
    
#     print(f"User {db_user.name} logged in successfully!")
#     return db_user


# def reset_password(db: Session, email: str, otp: str, new_password: str):
#     from crud.otp import verify_otp

#     verify_otp(db, email, otp)
#     user = db.query(User).filter(User.email == email).first()
#     user.hashed_password = hash_password(new_password)
#     db.commit()
#     return {"message": "Password reset successful"}
