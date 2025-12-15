from sqlalchemy.orm import Session
from models.playlists_model import Playlist
from fastapi import HTTPException
import uuid

class ListeningHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_listening_history_as_playlist(self, user_id):
        db_history_playlist = Playlist(owner_id=user_id, title="История прослушивания")
        self.db.add(db_history_playlist)
        self.db.commit()
        self.db.refresh(db_history_playlist)
