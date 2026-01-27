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
    total_files = 0
    total_questions = 0
    
    for s in all_stats:
        if s.files_uploaded_count:
            total_files += s.files_uploaded_count
        if s.questions_asked_count:
            total_questions += s.questions_asked_count

    # Step 1: Select the fields you want
    query = db.query(
        User.id,
        User.name,
        User.email,
        UserStats.files_uploaded_count,
        UserStats.questions_asked_count
    )
    #-left outer join for each user, SQLAlchemy will try to find matching stats where user_id equals that user’s ID.
    # Step 2: Join UserStats to User
    query = query.outerjoin(UserStats, User.id == UserStats.user_id)
    # Step 3: Order by User ID
    query = query.order_by(User.id.asc())
    # Step 4: Execute and get results
    results = query.all()

    # Format response

    user_stats = []
    for r in results:
        user_stats.append({
            "user_id": r.id,
            "name": r.name,
            "email": r.email,
            "files_uploaded_count": r.files_uploaded_count or 0,
            "questions_asked_count": r.questions_asked_count or 0
            })


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
