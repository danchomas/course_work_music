from datetime import datetime
from sqlalchemy.orm import Session
from models.track_model import Track
from models.profile_model import Profile
from fastapi import HTTPException
from core.s3_client import s3
import uuid

class TrackCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_track(self, title: str, user_id: int, music_file, date_and_time: datetime) -> Track:
        owner = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not owner:
            raise HTTPException(
                status_code=401,
                detail="У вас нету профиля артиста. Перед загрузкой треков, создайте себе профиль",
            )

        existing_track = (
            self.db.query(Track)
            .filter(Track.owner == owner.id, Track.title == title)
            .first()
        )
        if existing_track:
            raise HTTPException(
                status_code=409,
                detail="У вашего профиля был обнаружен трек с таким же названием.",
            )

        file_extension = music_file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        s3_key = f"{owner.nickname}/{title}/{unique_filename}"

        try:
            s3.upload_file(music_file.file, s3_key)
        except Exception:
            raise HTTPException(status_code=500, detail="Не удалось загрузить файл в облачное хранилище")

        db_track = Track(
            title=title,
            music_file_url=s3_key,
            owner=owner.id,
            release_date=date_and_time
        )
        self.db.add(db_track)
        self.db.commit()
        self.db.refresh(db_track)
        return db_track


class TrackPlayManager:
    def __init__(self, db: Session):
        self.db = db

    def play_track(self, artist_nickname, trackname):
        owner = self.db.query(Profile).filter(Profile.nickname == artist_nickname).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Артист не найден")

        track = self.db.query(Track).filter(Track.owner == owner.id, Track.title == trackname).first()
        if not track:
            raise HTTPException(status_code=404, detail="Трек не найден")

        file_stream = s3.get_file_object(track.music_file_url)

        if not file_stream:
            raise HTTPException(status_code=500, detail="Ошибка чтения файла из облака")

        return file_stream


class TrackGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_track_by_id(self, artist_nickname: str, trackname: str) -> Track:
        owner = (
            self.db.query(Profile).filter(Profile.nickname == artist_nickname).first()
        )
        if not owner:
             raise HTTPException(status_code=404, detail="Артист не найден")

        track = (
            self.db.query(Track)
            .filter(Track.owner == owner.id, Track.title == trackname)
            .first()
        )
        return track
