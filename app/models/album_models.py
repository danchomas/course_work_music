import uuid

from sqlalchemy.sql.schema import CheckConstraint, UniqueConstraint
from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class Album(Base):
    __tablename__ = "albums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("profiles.id"))

    cover_id = Column(UUID(as_uuid=True), ForeignKey("titles.id"))


class AlbumTrack(Base):
    __tablename__ = "album_track"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id"))
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"))

class AlbumRating(Base):
    __tablename__ = "album_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "album_id", name="uq_album_user_rating"),
        CheckConstraint("rating >= 1 AND rating <= 10", name="check_rating_album")
    )
