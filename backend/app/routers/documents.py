import os
import uuid
from datetime import datetime

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.core.security import get_current_user, require_role
from app.core.database import (
    get_session_for_category,
    SessionLocal,
    VALID_CATEGORIES,
)
from app.models.document import Document
from app.services.ai_service import analyze_document, AIServiceError


router = APIRouter()

def require_reviewer_or_admin(
    current_user: dict = Depends(get_current_user),
):
    roles = current_user.get("roles", [])

    if (
        "revisor_documental" not in roles
        and "admin_documental" not in roles
    ):
        raise HTTPException(
            status_code=403,
            detail="Se requiere el rol de revisor o administrador",
        )

    return current_user

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    current_user: dict = Depends(get_current_user),
):
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Categoría inválida. Use: {VALID_CATEGORIES}",
        )

    allowed_extensions = [".pdf", ".docx", ".doc"]
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Extensión no permitida. Use: {allowed_extensions}",
        )

    os.makedirs(settings.upload_dir, exist_ok=True)

    document_id = str(uuid.uuid4())
    saved_filename = f"{document_id}{file_extension}"
    saved_path = os.path.join(settings.upload_dir, saved_filename)

    with open(saved_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    db = get_session_for_category(category)

    try:
        new_document = Document(
            id=document_id,
            original_filename=file.filename,
            stored_path=saved_path,
            category=category,
            status="recibido",
            uploaded_by=current_user["username"],
            uploaded_at=datetime.utcnow(),
        )

        db.add(new_document)
        db.commit()

    finally:
        db.close()

    return {
        "id": document_id,
        "original_filename": file.filename,
        "category": category,
        "status": "recibido",
        "uploaded_by": current_user["username"],
    }

def _serialize(doc: Document, with_ai: bool = True) -> dict:
    data = {
        "id": doc.id,
        "original_filename": doc.original_filename,
        "category": doc.category,
        "status": doc.status,
        "uploaded_by": doc.uploaded_by,
        "uploaded_at": (
            doc.uploaded_at.isoformat()
            if doc.uploaded_at
            else None
        ),
        "reviewed_by": doc.reviewed_by,
        "reviewed_at": (
            doc.reviewed_at.isoformat()
            if doc.reviewed_at
            else None
        ),
        "review_comment": doc.review_comment,
    }

    if with_ai:
        data["ai_analysis"] = doc.ai_analysis
        data["ai_analyzed_at"] = (
            doc.ai_analyzed_at.isoformat()
            if doc.ai_analyzed_at
            else None
        )

    return data

@router.get("/")
def list_documents(
    current_user: dict = Depends(get_current_user),
):
    roles = current_user.get("roles", [])

    is_privileged = (
        "revisor_documental" in roles
        or "admin_documental" in roles
    )

    db = SessionLocal()

    try:
        query = db.query(Document)

        if not is_privileged:
            query = query.filter(
                Document.uploaded_by == current_user["username"]
            )

        docs = (
            query
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    finally:
        db.close()

    return {
        "total": len(docs),
        "documents": [
            _serialize(doc, with_ai=is_privileged)
            for doc in docs
        ],
    }

@router.get("/archive")
def list_archived_documents(
    current_user: dict = Depends(require_reviewer_or_admin),
):
    db = SessionLocal()

    try:
        approved_docs = (
            db.query(Document)
            .filter(Document.status == "aprobado")
            .order_by(Document.uploaded_at.desc())
            .all()
        )

        rejected_docs = (
            db.query(Document)
            .filter(Document.status == "rechazado")
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    finally:
        db.close()

    return {
        "approved": [
            _serialize(doc)
            for doc in approved_docs
        ],
        "rejected": [
            _serialize(doc)
            for doc in rejected_docs
        ],
        "total_approved": len(approved_docs),
        "total_rejected": len(rejected_docs),
    }

VALID_TRANSITIONS = {
    "recibido": ["en_revision"],
    "en_revision": ["revisado", "correccion"],
    "correccion": ["en_revision"],
    "revisado": ["aprobado", "rechazado"],
    "aprobado": ["en_revision"],
    "rechazado": ["en_revision"],
}


class ReviewRequest(BaseModel):
    comment: Optional[str] = None
    new_status: str

def _find_document(document_id: str):
    db = SessionLocal()

    doc = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if doc:
        return doc, db

    db.close()

    raise HTTPException(
        status_code=404,
        detail="Documento no encontrado",
    )

@router.post("/{document_id}/review")
def review_document(
    document_id: str,
    body: ReviewRequest,
    current_user: dict = Depends(require_reviewer_or_admin),
):
    doc, db = _find_document(document_id)

    try:
        allowed_transitions = VALID_TRANSITIONS.get(
            doc.status,
            [],
        )

        if body.new_status not in allowed_transitions:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Transición inválida: "
                    f"{doc.status} -> {body.new_status}"
                ),
            )

        allowed_review_statuses = (
            "en_revision",
            "revisado",
            "correccion",
        )

        if body.new_status not in allowed_review_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Este endpoint solamente permite "
                    "estados de revisión"
                ),
            )

        doc.status = body.new_status
        doc.reviewed_by = current_user["username"]
        doc.reviewed_at = datetime.utcnow()

        if body.comment:
            doc.review_comment = body.comment

        db.commit()

        return _serialize(doc)

    finally:
        db.close()

@router.post("/{document_id}/decide")
def decide_document(
    document_id: str,
    body: ReviewRequest,
    current_user: dict = Depends(
        require_role("admin_documental")
    ),
):
    doc, db = _find_document(document_id)

    try:
        if body.new_status not in VALID_TRANSITIONS.get(
            doc.status,
            [],
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Transición inválida: "
                    f"{doc.status} -> {body.new_status}"
                ),
            )

        if body.new_status not in (
            "aprobado",
            "rechazado",
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Solo aprobado/rechazado "
                    "permitido aquí"
                ),
            )

        doc.status = body.new_status
        doc.reviewed_by = current_user["username"]
        doc.reviewed_at = datetime.utcnow()

        if body.comment:
            doc.review_comment = body.comment

        db.commit()

        return _serialize(doc)

    finally:
        db.close()

@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    current_user: dict = Depends(
        require_reviewer_or_admin
    ),
):
    doc, db = _find_document(document_id)

    try:
        stored_path = doc.stored_path
        original_filename = doc.original_filename

    finally:
        db.close()

    if not stored_path:
        raise HTTPException(
            status_code=404,
            detail="El documento no tiene un archivo asociado",
        )

    if not os.path.isfile(stored_path):
        raise HTTPException(
            status_code=404,
            detail="El archivo físico no existe",
        )

    return FileResponse(
        path=stored_path,
        filename=original_filename,
        media_type="application/octet-stream",
    )

@router.post("/{document_id}/analyze")
def analyze(
    document_id: str,
    current_user: dict = Depends(require_reviewer_or_admin),
):
    doc, db = _find_document(document_id)

    try:
        doc.ai_analysis = analyze_document(
            doc.original_filename,
            doc.category,
            doc.stored_path,
        )

        doc.ai_analyzed_at = datetime.utcnow()

        db.commit()

        result = _serialize(doc)
        result["ai_notice"] = (
            "Recomendación de IA: no modifica el estado del "
            "documento y requiere validación humana."
        )
        return result

    except AIServiceError as e:
        db.rollback()
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )

    finally:
        db.close()

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user: dict = Depends(
        require_reviewer_or_admin
    ),
):
    doc, db = _find_document(document_id)

    try:
        stored_path = doc.stored_path

        db.delete(doc)
        db.commit()

    finally:
        db.close()
    if stored_path and os.path.exists(stored_path):
        try:
            os.remove(stored_path)
        except OSError:
            pass

    return {
        "message": "Documento eliminado",
        "id": document_id,
    }