import uuid
from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class Album(Base):
    __tablename__ = "albums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("profiles.id"))


class AlbumTrack(Base):
    __tablename__ = "album_track"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id"))
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"))
