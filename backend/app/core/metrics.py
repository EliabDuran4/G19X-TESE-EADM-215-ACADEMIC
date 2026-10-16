from sqlalchemy import func
from opentelemetry import metrics
from opentelemetry.metrics import Observation

from app.core.database import SessionLocal
from app.models.document import Document

STATUSES = [
    "recibido",
    "en_revision",
    "correccion",
    "revisado",
    "aprobado",
    "rechazado",
]

meter = metrics.get_meter("documental.proceso")

_uploaded = meter.create_counter(
    "documents_uploaded",
    unit="1",
    description="Documentos subidos por categoría",
)

_transitions = meter.create_counter(
    "document_status_transitions",
    unit="1",
    description="Transiciones de estado de documentos",
)

_decision_seconds = meter.create_histogram(
    "document_decision_duration_seconds",
    unit="s",
    description="Tiempo entre recibido y decisión final",
)


def _documents_by_status(options):
    db = SessionLocal()
    try:
        rows = (
            db.query(Document.status, func.count(Document.id))
            .group_by(Document.status)
            .all()
        )
    except Exception:
        return []
    finally:
        db.close()

    counts = dict(rows)
    return [
        Observation(counts.get(s, 0), {"status": s})
        for s in STATUSES
    ]


meter.create_observable_gauge(
    "documents_by_status",
    callbacks=[_documents_by_status],
    unit="1",
    description="Documentos actuales por estado",
)


def record_upload(category: str):
    _uploaded.add(1, {"category": category})


def record_transition(from_status: str, to_status: str):
    _transitions.add(
        1,
        {"from_status": from_status, "to_status": to_status},
    )


def record_decision_duration(
    seconds: float, decision: str, category: str
):
    _decision_seconds.record(
        seconds,
        {"decision": decision, "category": category},
    )