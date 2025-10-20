from sqlalchemy import Column, String, Integer, ForeignKey
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Track(Base):
    __tablename__ = "tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    music_file_url = Column(String, unique=True, nullable=False)
    owner = Column(Integer, ForeignKey("profiles.id"), nullable=False)
