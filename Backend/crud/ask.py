from sqlalchemy.orm import Session
from Backend.services.ask_service import process_query

def get_answer(query: str, user_id: int, db: Session) -> str:
    """
    CRUD wrapper for answering user queries.
    Delegates actual logic to ask_service.
    """
    
    return process_query(query, user_id, db)