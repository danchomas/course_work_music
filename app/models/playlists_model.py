from sqlalchemy import Table, Column, String, ForeignKey
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

platlist_tacks = Table(
    "playlist_track",
    Base.metadata,
    Column("track_id", UUID(as_uuid=True), ForeignKey("tracks.id")),
    Column("playlist_id", UUID(as_uuid=True), ForeignKey("playlists.id")),
)


class Playlists(Base):
    __tablename__ = "playlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    descriprion = Column(String)
