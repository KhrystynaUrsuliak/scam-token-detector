from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from app.database import get_db
from app.ml.predictor import predict_token
from app.models.token import Token
from app.models.check import Check
from app.models.user import User
from app.utils.dependencies import get_current_user
from app.services.market_data_service import get_token_market_data

router = APIRouter(prefix="/predict", tags=["Prediction"])


class PredictionRequest(BaseModel):
    name: str
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        return v


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

    market_data = get_token_market_data(
        name=request.name,
        slug=slug,
        include_chart=result["prediction"] == "LEGIT" or result["risk_score"] < 40
    )
    
    result["market_data"] = market_data

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
    
    result["token_id"] = token.id

    return result