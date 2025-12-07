from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    UploadFile,
    File,
    Form,
    Depends,
)
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from services.track_services import (
    TrackCreateManager,
    TrackGetManager,
    TrackPlayManager,
)
from datetime import datetime
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/upload_track")
def upload_track(
    file: UploadFile = File(...),
    title: str = Form(...),
    day: int = Form(..., ge=1, le=31, description="День (1-31)"),
    month: int = Form(..., ge=1, le=12, description="Месяц (1-12)"),
    year: int = Form(..., ge=1900, le=2100, description="Год"),
    hour: int = Form(0, ge=0, le=23, description="Час (0-23)"),
    minute: int = Form(0, ge=0, le=59, description="Минута (0-59)"),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")

    try:
        release_date = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Некорректная дата: {str(e)}"
        )

    track = TrackCreateManager(db).create_track(title, user_id, file, release_date)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Файл успешно загружен",
            "track_id": str(track.id),
            "release_date": release_date.strftime('%Y-%m-%d %H:%M')
        },
    )


@router.get("/play/{artist_nickname}/{trackname}")
def play_track(
    db: Session = Depends(get_db),
    artist_nickname: str = Path(...),
    trackname: str = Path(...),
):
    file_stream = TrackPlayManager(db).play_track(artist_nickname, trackname)
    return StreamingResponse(content=file_stream, media_type="audio/mpeg")


@router.post("/get_track_id")
def get_track_id(
    db: Session = Depends(get_db),
    artist_nickname: str = Form(...),
    trackname: str = Form(...),
):
    track = TrackGetManager(db).get_track_by_id(artist_nickname, trackname)
    if not track:
        raise HTTPException(status_code=404, detail="Такой трек не был найден")

    return JSONResponse(
        status_code=200, content={"message": "Успех", "track_id": str(track.id)}
    )
