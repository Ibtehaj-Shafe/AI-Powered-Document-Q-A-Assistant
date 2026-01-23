from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from Backend.database.database import get_db
from Backend.schemas.user import UserResponse
from Backend.crud import user as user_crud
from Backend.dependencies.jwt_dependency import get_current_user
from Backend.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.get_all_users(db)