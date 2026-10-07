import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String(500), nullable=False)
    stored_path = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="recibido")
    uploaded_by = Column(String(200), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(String(200), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    review_comment = Column(String(1000), nullable=True)
    ai_analysis = Column(Text, nullable=True)
    ai_analyzed_at = Column(DateTime, nullable=True)