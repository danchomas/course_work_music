import uuid
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    UploadFile,
    File,
    Form,
    Depends,
)
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from models.track_model import TrackRatings
from routers.user_routers import router
from services.track_services import (
    TrackCreateManager,
    TrackGetManager,
    TrackPlayManager,
    TrackRateService,
)
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/upload_track")
def upload_track(
    music_file: UploadFile = File(...),
    cover_file: UploadFile = File(...),
    title_track: str = Form(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    track = TrackCreateManager(db).create_track(title_track, user_id, music_file, cover_file)
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


@router.post("/rate_track")
def rate_the_track(
    rating: int = Form(...),
    track_id: str = Form(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="для оценки трека необходимо авторизоваться"
        )
    track_rating = TrackRateService(db).rate_track(user_id, track_id, rating)
    return track_rating
