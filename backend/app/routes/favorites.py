from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.favorite import Favorite
from app.models.token import Token
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/{token_id}")
def add_favorite(
    token_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    token = db.query(Token).filter(Token.id == token_id).first()

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    existing = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.token_id == token_id
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Token already in favorites")

    favorite = Favorite(
        user_id=current_user.id,
        token_id=token_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return {"message": "Token added to favorites", "favorite_id": favorite.id}


@router.get("/")
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = (
        db.query(Favorite, Token)
        .join(Token, Favorite.token_id == Token.id)
        .filter(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )

    return [
        {
            "favorite_id": favorite.id,
            "token_id": token.id,
            "name": token.name,
            "url": token.url,
            "slug": token.slug,
            "created_at": favorite.created_at
        }
        for favorite, token in results
    ]


@router.delete("/{token_id}")
def delete_favorite(
    token_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.token_id == token_id
        )
        .first()
    )

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()

    return {"message": "Token removed from favorites"}