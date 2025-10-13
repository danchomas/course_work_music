from fastapi import APIRouter, Depends, HTTPException, status, Path, Security, Body
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from schemas.profile_schemas import (
    ProfileCreateSchema,
    ProfileSchema
)
from services.profile_services import (
    ProfileCreateManager,
)
from core.database import get_db
from core.security import auth

router = APIRouter()

@router.post("/create_profile", dependencies=[Security(auth.verify_token)])
def create_profile(
    new_profile: ProfileCreateSchema = Body(...),
    db: Session = Depends(get_db)
) -> ProfileSchema:
    profile = ProfileCreateManager(db).create_profile(new_profile)
    return profile