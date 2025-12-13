import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.album_models import Album, AlbumTrack
from models.track_model import Track
from models.profile_model import Profile

class AlbumCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_album(self, title: str, user_id: int) -> Album:
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=403, detail="Только артисты с профилем могут создавать альбомы")

        db_album = Album(title=title, owner_id=profile.id)
        self.db.add(db_album)
        self.db.commit()
        self.db.refresh(db_album)
        return db_album

    def autocreate_album(self, title: str, user_id: int) -> Album:


class AlbumManager:
    def __init__(self, db: Session):
        self.db = db

    def add_track_to_album(self, album_id: uuid.UUID, track_id: uuid.UUID, user_id: int):
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=404, detail="Альбом не найден")

        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile or album.owner_id != profile.id:
            raise HTTPException(status_code=403, detail="Вы не являетесь владельцем этого альбома")

        track = self.db.query(Track).filter(Track.id == track_id).first()
        if not track:
            raise HTTPException(status_code=404, detail="Трек не найден")

        existing_link = self.db.query(AlbumTrack).filter(
            AlbumTrack.album_id == album_id,
            AlbumTrack.track_id == track_id
        ).first()

        if existing_link:
            raise HTTPException(status_code=409, detail="Трек уже добавлен в этот альбом")

        new_link = AlbumTrack(id=uuid.uuid4(), album_id=album_id, track_id=track_id)
        self.db.add(new_link)
        self.db.commit()
        return {"status": "Успех", "message": "Трек успешно добавлен"}

class AlbumGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_all_albums(self):
        return self.db.query(Album).all()

    def get_album_by_id(self, album_id: uuid.UUID):
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=404, detail="Альбом не найден")

        tracks_links = self.db.query(AlbumTrack).filter(AlbumTrack.album_id == album_id).all()
        track_ids = [link.track_id for link in tracks_links]

        return {
            "id": album.id,
            "title": album.title,
            "owner_id": album.owner_id,
            "tracks": track_ids
        }

    def get_my_albums(self, user_id: int):
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            return []
        return self.db.query(Album).filter(Album.owner_id == profile.id).all()
