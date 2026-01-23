from fastapi import APIRouter, Depends
from Backend.dependencies.jwt_dependency import require_admin
from Backend.models import User, UserStats
from sqlalchemy.orm import Session
from Backend.database.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Count total users
    total_users = db.query(User).count()

    all_stats = db.query(UserStats).all()

    total_files = sum(s.files_uploaded_count or 0 for s in all_stats)
    total_questions = sum(s.questions_asked_count or 0 for s in all_stats)

    # Fetch stats for all users (outer join ensures users without stats are included)
    results = (
    db.query(User.id, User.name, User.email,
             UserStats.files_uploaded_count,
             UserStats.questions_asked_count)
    .outerjoin(UserStats, User.id == UserStats.user_id)
    .order_by(User.id.asc())   # 👈 enforce ascending order
    .all()
)

    # Format response
    user_stats = [
        {
            "user_id": r.id,
            "name": r.name,
            "email": r.email,
            "files_uploaded_count": r.files_uploaded_count or 0,
            "questions_asked_count": r.questions_asked_count or 0
        }
        for r in results
    ]

    return {
        "message": f"Welcome To Admin Dashboard.",
        "total_users": total_users,
        "total_files_uploaded": total_files,
        "total_questions_asked": total_questions,
        
        "user_stats": user_stats
    }

# @router.get("/dashboard")
# def admin_dashboard(current_user: User = Depends(require_admin)):
#     return {"message": f"Welcome admin {current_user.name}, this is your dashboard."}



# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from Backend.database.database import get_db
# from Backend.dependencies.jwt_dependency import require_admin
# from Backend.crud import user_stat as stats_crud

# router = APIRouter(prefix="/admin", tags=["Admin"])


# @router.get("/stats")
# def admin_stats(
#     db: Session = Depends(get_db),
#     admin=Depends(require_admin),
# ):
#     return stats_crud.get_system_stats(db)
