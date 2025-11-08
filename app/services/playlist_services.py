from sqlalchemy.orm import Session
from models.playlists_model import Playlist
from fastapi import HTTPException


class PlaylistCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_playlis(self, title: str, description: str):
        db_playlist = Playlist(title=title, description=description)
        self.db.add(db_playlist)
        self.db.commit()
        self.db.refresh(db_playlist)
        return db_playlist
