from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml.predictor import predict_token
from app.models.token import Token
from app.models.check import Check
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])


class PredictionRequest(BaseModel):
    name: str
    url: str


@router.post("/")
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    slug = request.url.rstrip("/").split("/")[-1]

    token = db.query(Token).filter(Token.slug == slug).first()

    if not token:
        token = Token(
            name=request.name,
            url=request.url,
            slug=slug
        )
        db.add(token)
        db.commit()
        db.refresh(token)

    result = predict_token(request.name, request.url)

    check = Check(
        user_id=current_user.id,
        token_id=token.id,
        prediction_label=result["prediction"],
        risk_score=result["risk_score"],
        probability=result["probability"],
        explanation=result["explanation"]
    )

    db.add(check)
    db.commit()

    return result