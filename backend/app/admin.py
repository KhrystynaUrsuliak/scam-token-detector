from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import User, TokenCheck
from auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
        for user in users
    ]


@router.get("/checks")
def get_all_checks(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    checks = db.query(TokenCheck).order_by(TokenCheck.id.desc()).all()

    return [
        {
            "id": check.id,
            "user_id": check.user_id,
            "token_name": check.token_name,
            "token_url": check.token_url,
            "risk_score": check.risk_score,
            "is_scam": check.is_scam,
        }
        for check in checks
    ]


@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    total_users = db.query(User).count()
    total_checks = db.query(TokenCheck).count()
    scam_checks = db.query(TokenCheck).filter(TokenCheck.is_scam == True).count()

    scam_rate = 0
    if total_checks > 0:
        scam_rate = round((scam_checks / total_checks) * 100, 2)

    return {
        "total_users": total_users,
        "total_checks": total_checks,
        "scam_checks": scam_checks,
        "scam_rate": scam_rate,
    }