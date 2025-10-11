from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.profile_model import Profile
from sqlalchemy import select
from schemas.profile_schemas import UserCreateSchema
from uuid import UUID
from fastapi import HTTPException, status

class ProfileCreateManager:
    def __init__(self, db: Session):
        self.db = db
    
    def create_profile(self, profile: ProfileCreateSchema) -> Profile:
        existing_profile = self.db.query(Profile).filter(
            (Profile.nickname == profile.nikcname) | (Profile.user_id == profile.user_id)
        ).first()

        if existing_profile:
            if Profile.nickname == profile.nikcname:
                raise HTTPException(
                    status_code=401,
                    detail="К сожалению исполнитель с таким никнеймом уже создан!"
                )
            if Profile.user_id == profile.user_id:
                raise HTTPException(
                    status_code=401,
                    detail="Каждый пользователь может быть одновременно только одним исполнителем"
                )
        db_profile = Profile(
            nickname=profile.nickname,
            bio=profile.bio
        )
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
