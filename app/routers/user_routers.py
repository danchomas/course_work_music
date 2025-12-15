from fastapi import APIRouter, Depends, HTTPException, Path, Security, Body
from sqlalchemy.orm import Session
from typing import List

from services.like_services import LikesAsPlaylist
from schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserSchema,
    UserUpdateSchema,
)
from services.user_service import (
    UserCreateManager,
    UserLoginManager,
    UserGetManager,
    UserUpdateManager,
)
from services.listening_history_services import ListeningHistoryService
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.get("/all_users", dependencies=[Security(auth.verify_token)])
async def get_users(db: Session = Depends(get_db)) -> List[UserSchema]:
    users = UserGetManager(db).get_all_users()
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(
    user_id: int = Path(...), db: Session = Depends(get_db)
) -> UserSchema:
    user = UserGetManager(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="такого пользователя не существует")
    return user


@router.post("/create_user", response_model=UserSchema)
async def create_user(
    new_user: UserCreateSchema = Body(...), db: Session = Depends(get_db)
) -> UserSchema:
    user = UserCreateManager(db).create_user(new_user)
    if user:
        ListeningHistoryService(db).create_listening_history_as_playlist(user.id)
        LikesAsPlaylist(db).create_likes_playlist(user.id)
    return user


@router.post("/login")
async def login(creds: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    user = UserLoginManager(db).login_user(creds.username, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    token_values = {"username": user.username, "id": user.id}
    return {
        "access_token": auth.create_access_token(token_values),
        "token_type": "bearer",
    }


@router.post("/update_user", response_model=UserSchema)
async def update_user(
    creds: UserUpdateSchema = Body(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="вы передали невалидный токен")

    updated_user = UserUpdateManager(db).update_user(user_id, creds)
    return updated_user
