from sqlalchemy.orm import Session
from models.likes_model import Like
from fastapi import HTTPException
import uuid


class LikesManager:
    def __init__(self, db: Session):
        self.db = db

    def like_for_track_id(self, user_id: int, track_id: uuid) -> Like:
        existing_like = (
            self.db.query(Like)
            .filter(Like.user_id == user_id, Like.track_id == track_id)
            .first()
        )
        if existing_like:
            raise HTTPException(
                status_code=400, detail="Лайк на этот трек уже был поставлен"
            )
        db_like = Like(user_id=user_id, track_id=track_id)
        self.db.add(db_like)
        self.db.commit()
        self.db.refresh(db_like)
        return db_like
