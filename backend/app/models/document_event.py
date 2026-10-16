from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class DocumentEvent(Base):
    __tablename__ = "document_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String(36), nullable=False, index=True)
    previous_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    username = Column(String(200), nullable=False)
    comment = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)