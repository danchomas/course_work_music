from sqlalchemy.orm import Session
from models.playlists_model import Playlist
from fastapi import HTTPException


class PlaylistCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_playlis(self, title: str, description: str, user_id: int):
        db_playlist = Playlist(title=title, description=description, owner_id=user_id)
        self.db.add(db_playlist)
        self.db.commit()
        self.db.refresh(db_playlist)
        return db_playlist


class PlaylistGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_all_playlists(self):
        playlists = self.db.query(Playlist).all()
        return playlists

    def get_my_playlists(self, user_id: int):
        if user_id:
            return self.db.query(Playlist).filter(Playlist.owner_id == user_id).all()
        raise HTTPException(status_code=404, detail="у вас еще не нашлось плейлистов")
