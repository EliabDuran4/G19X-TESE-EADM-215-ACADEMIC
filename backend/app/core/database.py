from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

Base = declarative_base()

engine = create_engine(settings.database_url_documental)

SessionLocal = sessionmaker(bind=engine)

VALID_CATEGORIES = [
    "contratos_corporativo",
    "litigioso",
    "regulatorio_compliance",
    "propiedad_intelectual",
]

SHARD_MAP = {category: SessionLocal for category in VALID_CATEGORIES}
ENGINE_MAP = {"observabilidad_documental": engine}


def get_session_for_category(category: str):
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Categoría inválida: {category}")
    return SessionLocal()