from fastapi import APIRouter, Depends, Body, Form
from services.playlist_services import PlaylistCreateManager
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/playlists/create")
def create_playlist(
    db: Session = Depends(get_db), title: str = Form(...), description: str = Form(None)
):
    playlist = PlaylistCreateManager(db).create_playlis(title, description)
    return playlist
