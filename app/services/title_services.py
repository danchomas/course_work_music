import uuid
import os
from sqlalchemy.orm import Session
from models.title_models import Title

BASE_DIR = "files"

class TitleCreateService:
    def __init__(self, db: Session):
        self.db = db

    def create_cover_file(self, artist_nickname, file, track, album_id) -> uuid:
        cover_file_path = os.path.join(
            BASE_DIR, artist_nickname, track, file.filename
        )
        os.makedirs(os.path.dirname(cover_file_path), exist_ok=True)
        with open(cover_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        db_cover = Title(
            track_id=album_id,
            file_path=cover_file_path,
        )
        self.db.add(db_cover)
        self.db.commit()
        self.db.refresh(db_cover)
        return db_cover.id
