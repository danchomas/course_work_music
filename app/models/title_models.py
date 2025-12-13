import uuid
from sqlalchemy import UUID, Column, String, Integer, Enum, ForeignKey
from core.database import Base

class Title(Base):
    __tablename__ = "titles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id"), unique=True)

    file_path = Column(String, unique=True, nullable=False)
