from pydantic import BaseModel
from models.genre_models import Genres

class GenreSchema(BaseModel):
    track_id: str
    genre: Genres
