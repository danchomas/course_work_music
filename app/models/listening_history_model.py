from sqlalchemy import ForeignKey, Column, UUID, Integer, DateTime
from core.database import Base
from datetime import datetime
import uuid

class ListeningHistory(Base):
    __tablename__ = "listening_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id"), nullable=False)
    played_at = Column(DateTime, default=datetime.utcnow)
