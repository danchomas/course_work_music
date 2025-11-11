from sqlalchemy import Column, String, ForeignKey, Integer
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class PlaylistTrack(Base):
    __tablename__ = "playlist_track"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"), nullable=False)
    playlist_id = Column(UUID(as_uuid=True), ForeignKey("playlists.id"), nullable=False)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
