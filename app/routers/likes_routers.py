from fastapi import APIRouter, Depends, Body, Form
from services.like_services import LikesGetManager, LikesManager
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/like/{track_id}")
def like_track(
    track_id: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    like = LikesManager(db).like_for_track_id(user_id, track_id)
    return like


@router.get("/like/my_likes")
def get_my_likes(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
):
    user_id = payload.get("id")
    my_likes = LikesGetManager(db).get_my_likes(user_id)
    return my_likes
