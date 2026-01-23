from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.database.database import get_db
from Backend.models.user import User
from Backend.schemas.ask import AskResponse, AskRequest
from Backend.crud.ask import get_answer
from Backend.dependencies.jwt_dependency import require_user

router = APIRouter(prefix="/ask", tags=["ask"])

@router.post("/", response_model=AskResponse)
async def ask_question(
    payload: AskRequest,   # 👈 expects JSON body { "query": "..." }
    current_user: User = Depends(require_user),   # enforce JWT
    db: Session = Depends(get_db)
):
    """
    FastAPI route for user queries.
    - Accepts a JSON body with 'query'
    - Uses authenticated user_id from JWT
    - Delegates to CRUD/service for retrieval + LLM response
    """
    try:
        answer = get_answer(payload.query, current_user.id, db)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from Backend.database.database import get_db
# from Backend.schemas.ask import AskResponse
# from Backend.crud.ask import get_answer

# router = APIRouter(prefix="/ask", tags=["ask"])

# @router.post("/", response_model=AskResponse)
# async def ask_question(query: str, user_id: int, db: Session = Depends(get_db)):
#     """
#     FastAPI route for user queries.
#     - Accepts a query string + user_id
#     - Delegates to CRUD/service for retrieval + LLM response
#     """
#     try:
#         answer = get_answer(query, user_id, db)
#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))