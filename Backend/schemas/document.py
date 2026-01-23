from pydantic import BaseModel
from datetime import datetime

class CreateDocument(BaseModel):
    filename: str
    content: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    user_id: int
    upload_date: datetime

    class Config:
        from_attributes = True