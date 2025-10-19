from fastapi import (
    APIRouter,
    Path,
    UploadFile,
    File,
    Form,
    Query,
    Depends,
    HTTPException,
    Security,
    Body,
)
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse, FileResponse
from pydantic.root_model import RootModelRootType
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
import os

from starlette.types import HTTPExceptionHandler

from routers.user_routers import router
from schemas.track_schemas import (
    TrackCreateSchema,
    TrackResponseSchema,
)

from services.track_services import TrackCreateManager, TrackPlayManager
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/upload_track")
def upload_track(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    track = TrackCreateManager(db).create_track(title, user_id, file)
    return JSONResponse(
        status_code=200,
        content={"message": "Файл успешно загружен", "track_id": str(track.id)},
    )


@router.get("/play/{artist_nickname}/{trackname}")
def play_track(
    db: Session = Depends(get_db),
    artist_nickname: str = Path(...),
    trackname: str = Path(...),
):
    track_for_playing = TrackPlayManager(db).play_track(artist_nickname, trackname)
    return FileResponse(track_for_playing, media_type="audio/mpeg")
