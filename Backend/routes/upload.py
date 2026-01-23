from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from sqlalchemy.orm import Session
from Backend.database.database import get_db
from Backend.models.user import User
from Backend.schemas.document import DocumentResponse
from Backend.crud.upload import create_document
from Backend.services.upload_service import extract_text_from_pdf, extract_text_from_docx
from Backend.dependencies.jwt_dependency import require_user

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/", response_model=DocumentResponse)
async def upload_file(
    file: UploadFile = File(...),  # 👈 file upload  tells FastAPI the type of data you expect (an uploaded file object).
    current_user: User = Depends(require_user),   # 👈 enforce JWT
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()

        # Only allow PDF and DOCX
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(content)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(content)
        else:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported."
            )
        # Save document tied to authenticated user
        doc = create_document(text, file.filename, current_user.id, db)
        return doc

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))