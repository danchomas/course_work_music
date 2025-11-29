import uuid

from pydantic import BaseModel


class TrackCreateSchema(BaseModel):
    title: str


class TrackResponseSchema(BaseModel):
    id: int
    title: str
    music_file_url: str
    owner_id: int


class AddTrackToPlaylistSchema(BaseModel):
    playlist_id: uuid.UUID
    track_id: uuid.UUID
