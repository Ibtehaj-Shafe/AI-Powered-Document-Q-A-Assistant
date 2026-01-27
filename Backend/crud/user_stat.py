from sqlalchemy.orm import Session
from Backend.models import User
from Backend.models import UserStats


def get_system_stats(db: Session):
    total_users = db.query(User).count()

    # - .with_entities(...) → selects only specific columns instead of the whole object
    
    totals = db.query(
        UserStats
    ).with_entities(
        UserStats.files_uploaded_count,
        UserStats.questions_asked_count
    ).all()

    return {
        "total_users": total_users,
        "total_documents": sum(x.files_uploaded_count for x in totals),
        "total_questions": sum(x.questions_asked_count for x in totals),
    }
