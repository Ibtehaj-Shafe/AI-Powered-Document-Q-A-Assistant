from sqlalchemy.orm import Session
from Backend.models.document import Document
from Backend.services.upload_service import process_upload

def create_document(file_content: str, filename: str, user_id: int, db: Session) -> Document:
    """
    CRUD function to handle document creation.
    Delegates the actual processing to upload_service.
    """
    return process_upload(file_content, filename, user_id, db)