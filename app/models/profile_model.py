from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.sql import func
from core.database import Base

class VerifiedStatus(Enum):
    NOT_VERIFIED = "not_verified"
    CHECK_VERIFIED = "verified_in_progress"
    VERIFIED = "verified"



class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, nullable=False)
    nickname = Column(String, nullable=False, unique=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    is_verified = Column(Enum(VerifiedStatus), nullable=False, default=VerifiedStatus.NOT_VERIFIED)


