from sqlalchemy import Column, String, UUID, ForeignKey, Integer, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base
import uuid

class Track(Base):
    __tablename__ = "tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    music_file_url = Column(String, unique=True, nullable=False)
    owner = Column(Integer, ForeignKey("profiles.id"), nullable=False)

    likes = relationship("Like", back_populates="track")

class TrackRatings(Base):
    __tablename__ = "track_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "track_id", name="uq_user_track_rating"),
        CheckConstraint("rating >= 1 AND rating <= 10", name="check_rating_range"),
    )
