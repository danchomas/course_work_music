from pydantic import BaseModel


class TrackCreateSchema(BaseModel):
    title: str


class TrackResponseSchema(BaseModel):
    id: int
    title: str
    music_file_url: str
    owner_id: int
