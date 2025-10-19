from fastapi import (
    APIRouter,
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

from services.track_services import TrackCreateManager
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
def play_track(artist_nickname: str, trackname: str):
    file_path = os.path.join("files", artist_nickname, trackname)
    if os.path.exists(file_path):
        for file in os.listdir(file_path):
            if file.endswith(".mp3"):
                mp3_file = os.path.join(file_path, file)
                return FileResponse(mp3_file, media_type="audio/mpeg")
    else:
        raise HTTPException(
            status_code=404, detail="К сожалению данная композиция не была найдена"
        )
