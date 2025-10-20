from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class Likes(Base):
    __tablename__ = "likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "track_id", name="unique_user_track_like"),
    )

    user = relationship("Users", back_populates="likes")
    track = relationship("Tracks", back_populates="likes")
