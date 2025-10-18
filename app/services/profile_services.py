from sqlalchemy.orm import Session
from models.profile_model import Profile
from schemas.profile_schemas import ProfileCreateSchema
from fastapi import HTTPException


class ProfileCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, profile: ProfileCreateSchema, user_id: int) -> Profile:
        existing_profile = (
            self.db.query(Profile)
            .filter((Profile.nickname == profile.nickname))
            .first()
        )

        if existing_profile:
            if Profile.nickname == profile.nickname:
                raise HTTPException(
                    status_code=401,
                    detail="К сожалению исполнитель с таким никнеймом уже создан!",
                )
        db_profile = Profile(
            nickname=profile.nickname, bio=profile.bio, user_id=user_id
        )
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile


class ProfileGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_all_profiles(self) -> list[Profile]:
        return self.db.query(Profile).all()

    def get_user_profile(self, user_id: int) -> Profile:
        db_profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not db_profile:
            raise HTTPException(
                status_code=401, detail="Вы пока не зарегистрировали себя как артист"
            )
        return db_profile
