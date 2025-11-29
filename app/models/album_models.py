from core.database import Base
from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Album(Base):
    __tablename__ = "albums"

    id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("profiles.id"))


class AlbumTrack(Base):
    __tablename__ = "album_track"

    id = Column(UUID, primary_key=True)
    album_id = Column(UUID, ForeignKey("albums.id"))
    track_id = Column(UUID, ForeignKey("tracks.id"))
