from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Path,
    Security,
    Body,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas.track_schemas import TrackCreateSchema, TrackResponseSchema
from services.track_services import TrackCreateManager
from services.profile_services import ProfileGetManager
from core.database import get_db
from core.security import auth

router = APIRouter(prefix="/tracks", tags=["tracks"])


def verify_artist_profile(
    payload: dict = Depends(auth.verify_token), db: Session = Depends(get_db)
):
    """Зависимость для проверки наличия профиля артиста"""
    user_id = payload.get("id")
    profile_manager = ProfileGetManager(db)
    profile = profile_manager.get_user_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Для загрузки треков необходимо создать профиль артиста",
        )

    return {"user_id": user_id, "profile": profile}


@router.post(
    "/upload", response_model=TrackResponseSchema, status_code=status.HTTP_201_CREATED
)
async def upload_track(
    title: str = Form(..., description="Название трека"),
    music_file: UploadFile = File(..., description="MP3 файл трека"),
    cover_file: Optional[UploadFile] = File(
        None, description="Обложка трека (JPG/PNG)"
    ),
    db: Session = Depends(get_db),
    user_info: dict = Depends(verify_artist_profile),
):
    """
    Загрузка нового трека (только для пользователей с профилем артиста)
    """
    track_manager = TrackCreateManager(db)

    track = await track_manager.create_track(
        title=title,
        owner_id=user_info["user_id"],
        music_file=music_file,
        cover_file=cover_file,
    )

    return track


@router.get("/my_tracks", response_model=List[TrackResponseSchema])
async def get_my_tracks(
    db: Session = Depends(get_db), user_info: dict = Depends(verify_artist_profile)
):
    """Получение всех треков текущего артиста"""
    track_manager = TrackCreateManager(db)
    tracks = track_manager.get_user_tracks(user_info["user_id"])
    return tracks


@router.get("/{track_id}/file")
async def get_track_file(
    track_id: int = Path(..., description="ID трека"), db: Session = Depends(get_db)
):
    """Получение файла трека (доступно всем)"""
    track_manager = TrackCreateManager(db)
    return await track_manager.get_track_file(track_id)


@router.get("/{track_id}/cover")
async def get_track_cover(
    track_id: int = Path(..., description="ID трека"), db: Session = Depends(get_db)
):
    """Получение обложки трека (доступно всем)"""
    track_manager = TrackCreateManager(db)
    return await track_manager.get_track_cover(track_id)


@router.get("/artist/{profile_id}", response_model=List[TrackResponseSchema])
async def get_artist_tracks(
    profile_id: int = Path(..., description="ID профиля артиста"),
    db: Session = Depends(get_db),
):
    """Получение всех треков конкретного артиста"""
    track_manager = TrackCreateManager(db)
    tracks = track_manager.get_artist_tracks(profile_id)
    return tracks
