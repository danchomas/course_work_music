from fastapi import APIRouter, Depends, Body, Form
from services.playlist_services import PlaylistCreateManager, PlaylistGetManager
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/playlists/create")
def create_playlist(
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(None),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    playlist = PlaylistCreateManager(db).create_playlis(title, description, user_id)
    return playlist


@router.get("/playlists/get_all")
def get_all_playlists(
    db: Session = Depends(get_db),
):
    return PlaylistGetManager(db).get_all_playlists()


@router.get("/playlists/get_my_playlists")
def get_my_playlists(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    return PlaylistGetManager(db).get_my_playlists(payload.get("id"))
