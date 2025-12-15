from sqlalchemy.orm import Session
from models.likes_model import Like
from models.playlists_model import Playlist
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


class LikesGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_my_likes(self, user_id: int):
        likes = self.db.query(Like).filter(Like.user_id == user_id).all()
        if likes:
            return likes
        raise HTTPException(
            status_code=404, detail="Вы еще не поставили ни одного лайка"
        )

class LikesAsPlaylist:
    def __init__(self, db: Session):
        self.db = db

    def create_likes_playlist(self, user_id):
        db_likes_playlist = Playlist(owner_id=user_id, title="Лайки")
        self.db.add(db_likes_playlist)
        self.db.commit()
        self.db.refresh(db_likes_playlist)
