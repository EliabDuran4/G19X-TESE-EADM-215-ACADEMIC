import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ["DATABASE_URL_REPORTING"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def query(sql: str, params: dict | None = None) -> list[dict]:
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]