from sqlalchemy import Column, ForeignKey, Enum, UUID
from core.database import Base
from enum import Enum as PyEnum
import uuid

class Genres(PyEnum):
    RAP = "rap"
    ROCK = "rock"
    CLASSIC = "classic"
    ELECTRO = "electro"
    SHANSON = "shanson  "

class TrackGenre(Base):
    __tablename__ = "track_genres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"), nullable=False)
    genre = Column(Enum(Genres), nullable=False)
