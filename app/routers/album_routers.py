from fastapi import APIRouter, Depends, Body, HTTPException, Security, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid

from core.database import get_db
from core.security import auth
from schemas.album_schemas import AlbumResponseSchema, AlbumTrackAddSchema
from services.album_services import AlbumCreateManager, AlbumGetManager, AlbumManager, AlbumRateService

router = APIRouter()

@router.post("/create")
def create_album(
    title: str = Form(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    return AlbumCreateManager(db).create_album(title, user_id)

@router.post("/add_track")
def add_track_to_album(
    data: AlbumTrackAddSchema = Body(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    return AlbumManager(db).add_track_to_album(data.album_id, data.track_id, user_id)

@router.get("/get_all", response_model=List[AlbumResponseSchema])
def get_all_albums(db: Session = Depends(get_db)):
    return AlbumGetManager(db).get_all_albums()

@router.get("/my_albums", response_model=List[AlbumResponseSchema])
def get_my_albums(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    return AlbumGetManager(db).get_my_albums(user_id)

@router.get("/{album_id}")
def get_album_details(
    album_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    return AlbumGetManager(db).get_album_by_id(album_id)

@router.post("rate_album")
def rate_the_album(
    album_id: uuid.UUID,
    rating: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="вы не авторизованы")

    rating = AlbumRateService(db).rate_album(user_id, album_id, rating)
    return rating
