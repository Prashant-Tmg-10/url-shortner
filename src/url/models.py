from src.utils.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime


class urlModel(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String)
    short_code = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    click_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, nullable=True)