import uuid

from core.database import get_db
from core.security import auth
from fastapi import APIRouter, Body, Depends, Form
from schemas.track_schemas import AddTrackToPlaylistSchema
from services.playlist_services import (
    PlaylistCreateManager,
    PlaylistGetManager,
    PlaylistTrackManager,
)
from sqlalchemy.orm import Session

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


@router.get("/playlists/{playlist_id}/tracks")
def get_tracks_from_playlist(
    playlist_id: uuid.UUID,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    playlist = PlaylistGetManager(db).get_all_tracks_playlist_id(playlist_id)
    return playlist


@router.post("/playlists/add_track_to_playlist")
def add_track(
    request: AddTrackToPlaylistSchema,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    return PlaylistTrackManager(db).add_track_to_playlist(
        request.track_id, request.playlist_id
    )
