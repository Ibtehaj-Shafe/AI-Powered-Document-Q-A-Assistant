from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Backend.database.database import get_db
from Backend.schemas.user import UserCreate, UserResponse, UserLogin
from Backend.schemas.auth import TokenResponse, RefreshRequest
from Backend.schemas.otp_reset import OTPResetCreate, OTPResetResponse,OTPResetRequest
from Backend.crud import user as user_crud, otp as otp_crud
from Backend.crud.auth import authenticate_user, refresh_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(user, db)

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return authenticate_user(db, user.email, user.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid email or password")

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db, body.refresh_token)

@router.post("/forgot-password")
def forgot_password(request: OTPResetCreate, db: Session = Depends(get_db)):
    return otp_crud.create_otp(db, request.email)

@router.post("/reset-password")
def reset_password(request: OTPResetRequest, db: Session = Depends(get_db)):
    return user_crud.reset_password(db, request.email, request.otp, request.new_password)

# router = APIRouter(prefix="/auth", tags=["Auth"])

# # ---------------------------- Signup ----------------------
# @router.post("/signup", response_model=UserResponse)
# def signup(user: UserCreate, db: Session = Depends(get_db)):
#     return user_crud.create_user(user, db)

# # ---------------------------- View Users ----------------------
# @router.get("/view", response_model=List[UserResponse])
# def signup( db: Session = Depends(get_db)):
#     return user_crud.get_all_users(db)

# # ---------------------------- Login ----------------------
# @router.post("/login", response_model=TokenResponse)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     try:
#         return user_crud.authenticate_user(db, user.email, user.password)
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid email or password")
# #-----------------------------Refresh Token----------------------

# @router.post("/refresh", response_model=TokenResponse)
# def refresh_token(body: RefreshRequest, db: Session = Depends(get_db)):
#     return refresh_access_token(db, body.refresh_token)


# # @router.post("/login", response_model=UserResponse)
# # def login(user: UserLogin , db: Session = Depends(get_db)):
# #     # return user_crud.login_user(user, db)

# # ---------------------------- Forgot Password ----------------------d
# @router.post("/forgot-password")
# def forgot_password(request: OTPResetCreate, db: Session = Depends(get_db)):
#     return otp_crud.create_otp(request, db)

# # ---------------------------- Reset Password ----------------------
# @router.post("/reset-password", response_model=OTPResetResponse)
# def reset_password(request: OTPResetResponse, db: Session = Depends(get_db)):
#     return otp_crud.reset_password(request, db)