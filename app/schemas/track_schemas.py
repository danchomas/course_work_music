# schemas/track_schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrackCreateSchema(BaseModel):
    title: str


class TrackResponseSchema(BaseModel):
    id: int
    title: str
    cover_url: str
    music_file_url: str
    owner: int
    created_at: datetime

    class Config:
        from_attributes = True
