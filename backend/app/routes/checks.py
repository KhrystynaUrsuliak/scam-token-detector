from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.check import Check
from app.models.token import Token
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/checks", tags=["Checks"])


@router.get("/")
def get_user_checks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    offset = (page - 1) * limit
    query = (
        db.query(Check, Token)
        .join(Token, Check.token_id == Token.id)
        .filter(Check.user_id == current_user.id)
        .order_by(Check.created_at.desc())
    )
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [
            {
                "check_id": check.id,
                "token_id": token.id,
                "name": token.name,
                "url": token.url,
                "slug": token.slug,
                "prediction": check.prediction_label,
                "risk_score": check.risk_score,
                "probability": check.probability,
                "explanation": check.explanation,
                "created_at": check.created_at
            }
            for check, token in results
        ]
    }