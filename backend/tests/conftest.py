import os
os.environ["DATABASE_URL_DOCUMENTAL"] = "sqlite://" 
os.environ["OTEL_SDK_DISABLED"] = "true"
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.routers.documents as docs_router
from app.core.database import Base
from app.core.security import get_current_user
from app.main import app
from app.models.document import Document


@pytest.fixture()
def db(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    monkeypatch.setattr(docs_router, "SessionLocal", Session)
    yield Session
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db):
    yield TestClient(app)  # sin "with": no dispara el startup
    app.dependency_overrides.clear()


@pytest.fixture()
def as_role():
    def _set(role):
        app.dependency_overrides[get_current_user] = lambda: {
            "username": f"{role}_test",
            "email": None,
            "roles": [role],
        }
    return _set


@pytest.fixture()
def make_doc(db):
    def _make(status="recibido",  reviewed_at=None):
        s = db()
        doc = Document(
            id="doc-1",
            original_filename="a.pdf",
            stored_path="uploads/a.pdf",
            category="litigioso",
            status=status,
            uploaded_by="usuario_test",
            uploaded_at=datetime.utcnow(),
            reviewed_at=reviewed_at or datetime.utcnow(),
        )
        s.add(doc)
        s.commit()
        s.close()
        return "doc-1"
    return _make