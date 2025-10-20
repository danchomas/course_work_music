from fastapi import APIRouter, Depends, Security, Body
from sqlalchemy.orm import Session
from typing import List

from schemas.profile_schemas import (
    ProfileCreateSchema,
    ProfileSchema,
    ProfileUserSchema,
)
from services.profile_services import ProfileCreateManager, ProfileGetManager
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/create_profile", dependencies=[Security(auth.verify_token)])
def create_profile(
    new_profile: ProfileCreateSchema = Body(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token),
) -> ProfileSchema:
    profile = ProfileCreateManager(db).create_profile(new_profile, payload["id"])
    return profile


@router.get("/get_all_profiles")
def get_all_profiles(db: Session = Depends(get_db)) -> List[ProfileUserSchema]:
    return ProfileGetManager(db).get_all_profiles()


@router.post("/get_my_profile")
def get_my_profile(
    db: Session = Depends(get_db), payload: dict = Depends(auth.verify_token)
) -> ProfileUserSchema:
    user_id = payload.get("id")
    return ProfileGetManager(db).get_user_profile(user_id)
