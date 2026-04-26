from fastapi import APIRouter, Depends
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
    current_user: User = Depends(get_current_user)
):
    results = (
        db.query(Check, Token)
        .join(Token, Check.token_id == Token.id)
        .filter(Check.user_id == current_user.id)
        .order_by(Check.created_at.desc())
        .all()
    )

    return [
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