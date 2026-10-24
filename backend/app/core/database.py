from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

Base = declarative_base()

engine = create_engine(
    settings.database_url_documental,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine)

VALID_CATEGORIES = [
    "contratos_corporativo",
    "litigioso",
    "regulatorio_compliance",
    "propiedad_intelectual",
]