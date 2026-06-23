from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.check import Check
from app.models.report import Report
from app.models.token import Token
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    offset = (page - 1) * limit
    query = db.query(User).order_by(User.id.desc())
    total = query.count()
    users = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            }
            for user in users
        ]
    }


@router.get("/checks")
def get_all_checks(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    offset = (page - 1) * limit
    query = db.query(Check).order_by(Check.id.desc())
    total = query.count()
    checks = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [
            {
                "id": check.id,
                "user_id": check.user_id,
                "token_id": check.token_id,
                "prediction_label": check.prediction_label,
                "risk_score": check.risk_score,
                "probability": check.probability,
                "explanation": check.explanation,
                "created_at": check.created_at,
            }
            for check in checks
        ]
    }


@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    total_users = db.query(User).count()
    total_checks = db.query(Check).count()

    scam_checks = (
        db.query(Check)
        .filter(Check.prediction_label.ilike("SCAM"))
        .count()
    )

    safe_checks = (
        db.query(Check)
        .filter(Check.prediction_label.ilike("LEGIT"))
        .count()
    )

    scam_rate = 0
    if total_checks > 0:
        scam_rate = round((scam_checks / total_checks) * 100, 2)

    return {
        "total_users": total_users,
        "total_checks": total_checks,
        "scam_checks": scam_checks,
        "safe_checks": safe_checks,
        "scam_rate": scam_rate,
    }


class ReportStatusUpdate(BaseModel):
    status: str


@router.get("/reports")
def get_all_reports(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    offset = (page - 1) * limit
    query = (
        db.query(Report, Token)
        .join(Token, Report.token_id == Token.id)
        .order_by(Report.created_at.desc())
    )
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [
            {
                "report_id": report.id,
                "user_id": report.user_id,
                "token_id": token.id,
                "token_name": token.name,
                "token_url": token.url,
                "comment": report.comment,
                "status": report.status,
                "created_at": report.created_at,
            }
            for report, token in results
        ]
    }


@router.patch("/reports/{report_id}")
def update_report_status(
    report_id: int,
    body: ReportStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    allowed_statuses = {"pending", "reviewed", "resolved", "rejected"}
    if body.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"status must be one of: {', '.join(sorted(allowed_statuses))}"
        )

    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = body.status
    db.commit()

    return {"message": "Report status updated", "report_id": report.id, "status": report.status}
