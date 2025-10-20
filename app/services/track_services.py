from sqlalchemy.orm import Session
from models.track_model import Track
from models.profile_model import Profile
from fastapi import HTTPException
import os

BASE_DIR = "files"


class TrackCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_track(self, track: str, user_id, music_file) -> Track:
        owner = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not owner:
            raise HTTPException(
                status_code=401,
                detail="У вас нету профиля артиста. Перед загрузкой треков, создайте себе профиль",
            )
        existing_track = (
            self.db.query(Track)
            .filter(Track.owner == owner.id, Track.title == track)
            .first()
        )
        if existing_track:
            raise HTTPException(
                status_code=409,
                detail="У вашего профиля был обнаружен трек с таким же названием. Придумайте новое, это не допускается",
            )

        owner_nickname = (
            self.db.query(Profile.nickname).filter(Profile.id == owner.id).scalar()
        )

        music_file_path = os.path.join(
            BASE_DIR, owner_nickname, track, music_file.filename
        )
        os.makedirs(os.path.dirname(music_file_path), exist_ok=True)

        with open(music_file_path, "wb") as buffer:
            buffer.write(music_file.file.read())

        db_track = Track(
            title=track,
            music_file_url=music_file_path,
            owner=owner.id,
        )
        self.db.add(db_track)
        self.db.commit()
        self.db.refresh(db_track)
        return db_track


class TrackPlayManager:
    def __init__(self, db: Session):
        self.db = db

    def play_track(self, artist_nickname, trackname):
        file_path = os.path.join("files", artist_nickname, trackname)
        if os.path.exists(file_path):
            for file in os.listdir(file_path):
                if file.endswith(".mp3"):
                    mp3_file = os.path.join(file_path, file)
                    return mp3_file
        else:
            raise HTTPException(
                status_code=404, detail="К сожалению данная композиция не была найдена"
            )
