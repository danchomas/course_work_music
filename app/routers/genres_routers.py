from fastapi import APIRouter, Depends, Body, Security, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid

from core.database import get_db
from core.security import auth
from schemas.genre_schemas import GenreSchema
from services.genre_services import GenreSetService

router = APIRouter()

@router.post("/set_genre")
def set_genre(
    genre_data: GenreSchema,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    genre = GenreSetService(db).set_genre_to_track(user_id, genre_data.genre, genre_data.track_id)
    return genre
