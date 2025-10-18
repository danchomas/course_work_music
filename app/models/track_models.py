from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class Track(Base):
    __tablename__ = "tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    track_name = Column(String)
    track_cover_url = Column(String, unique=True)
    track_url = Column(String, unique=True)
    track_owner = Column(Integer, ForeignKey="profiles.id")
