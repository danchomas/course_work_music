import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.genre_models import TrackGenre
from models.profile_model import Profile
from models.track_model import Track

class GenreSetService:
    def __init__(self, db: Session):
        self.db = db

    def set_genre_to_track(self, user_id: str, genre: str, track_id: uuid) -> TrackGenre:
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(
                status_code=403,
                detail="только пользователи с профилем артиста могут устанавливать жанры на свои треки"
            )

        track = self.db.query(Track).filter(Track.id==track_id).first()
        if not track:
            raise HTTPException(
                status_code=403,
                detail="не могу найти такой трек, может быть вы ошиблись"
            )

        if track.owner != profile.id:
            raise HTTPException(
                status_code=405,
                detail="вы не являетесь автором данного трека, поэтому не можете поставить ему жанр"
            )

        db_genre_track = TrackGenre(track_id=track_id, genre=genre)
        self.db.add(db_genre_track)
        self.db.commit()
        self.db.refresh(db_genre_track)

        return db_genre_track
