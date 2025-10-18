from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.track_models import Track
from sqlalchemy import select
from schemas.profile_schemas import ProfileCreateSchema
from uuid import UUID
from fastapi import HTTPException, status


class TrackCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_track(self, track: TrackCreateSchema) -> Track:
        existing_track = (
            self.db.query(Track)
            .filter((Track.owner == track.owner_id and Track.title == track.title))
            .first()
        )
        if existing_track:
            raise HTTPException(
                status_code=409,
                detail="У вашего профиля был обнаружен трек с таким же названием. Придумайте новое, это не допускается",
            )
        db_track = Track(
            title=track.title,
            cover_url=f"files/{track.owner_id}/{track.title}/{track.title}.jpg",
            nusic_file_url=f"files/{track.owner_id}/{track.title}/{track.title}.mp3",
            owner=track.owner_id,
        )
        self.db.add(db_track)
        self.db.commit()
        self.db.refresh(db_track)
        return db_track
