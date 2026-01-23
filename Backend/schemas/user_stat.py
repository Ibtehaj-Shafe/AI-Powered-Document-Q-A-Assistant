from pydantic import BaseModel, EmailStr

class UserStatCreate(BaseModel):
    user_id: int
    files_uploaded_count: int
    questions_asked_count: int

class UserStatResponse(BaseModel):
    id: int
    user_id: int
    files_uploaded_count: int
    questions_asked_count: int

    class Config:
        from_attributes = True

        # orm_mode = True  # Enable ORM mode for compatibility with ORM objects