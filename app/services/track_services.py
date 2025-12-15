import uuid
from sqlalchemy.orm import Session
from starlette.types import HTTPExceptionHandler
from models.track_model import Track, TrackRatings
from models.profile_model import Profile
from models.track_model import TrackRatings
from fastapi import HTTPException
from .title_services import TitleCreateService
from .album_services import AlbumCreateManager
import os

BASE_DIR = "files"


class TrackCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_track(self, track: str, user_id, music_file, cover_file) -> Track:
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
        album = AlbumCreateManager(self.db).autocreate_album_for_single(track, owner.id, db_track.id)
        TitleCreateService(self.db).create_cover_file(owner_nickname, cover_file, track, album.id)
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


class TrackGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_track_by_id(self, artist_nickname: str, trackname: str) -> Track:
        owner = (
            self.db.query(Profile).filter(Profile.nickname == artist_nickname).first()
        )
        track = (
            self.db.query(Track)
            .filter(Track.owner == owner.id, Track.title == trackname)
            .first()
        )
        return track


class TrackRateService:
    def __init__(self, db: Session):
        self.db = db

    def rate_track(self, user_id: int, track_id: str, rating: int) -> TrackRatings:
        if rating > 10 or rating < 1:
            raise HTTPException(status_code=402, detail="оценка должна быть от 1 до 10")

        existent_relationship = self.db.query(TrackRatings).filter(TrackRatings.user_id == user_id, TrackRatings.track_id == track_id).first()
        if existent_relationship:
            raise HTTPException(status_code=402, detail="вы уже оценивали данный трек")

        db_rating = TrackRatings(user_id=user_id, track_id=track_id, rating=rating)
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating
