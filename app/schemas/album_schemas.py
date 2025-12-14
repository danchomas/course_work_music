import uuid
from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import List

class AlbumCreateSchema(BaseModel):
    title: str
    cover_file: UploadFile = File(...)

class AlbumTrackAddSchema(BaseModel):
    album_id: uuid.UUID
    track_id: uuid.UUID

class AlbumResponseSchema(BaseModel):
    id: uuid.UUID
    title: str
    owner_id: int

    class Config:
        from_attributes = True

class AlbumWithTracksSchema(AlbumResponseSchema):
    tracks: List[uuid.UUID] = []
