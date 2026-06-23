from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report import Report
from app.models.token import Token
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


class ReportRequest(BaseModel):
    comment: str | None = None


@router.post("/{token_id}")
def submit_report(
    token_id: int,
    body: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    token = db.query(Token).filter(Token.id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    report = Report(
        user_id=current_user.id,
        token_id=token_id,
        comment=body.comment,
        status="pending"
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {"message": "Report submitted", "report_id": report.id}


@router.get("/")
def get_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    offset = (page - 1) * limit
    query = (
        db.query(Report, Token)
        .join(Token, Report.token_id == Token.id)
        .filter(Report.user_id == current_user.id)
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
                "token_id": token.id,
                "token_name": token.name,
                "token_url": token.url,
                "comment": report.comment,
                "status": report.status,
                "created_at": report.created_at
            }
            for report, token in results
        ]
    }
