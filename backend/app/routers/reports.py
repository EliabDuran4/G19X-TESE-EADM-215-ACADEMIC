import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.core.security import require_role

router = APIRouter()

ADMIN_ROLE = "admin_documental"


async def _get(path: str):
    try:
        async with httpx.AsyncClient(timeout=settings.reporting_timeout) as client:
            response = await client.get(f"{settings.reporting_service_url}{path}")
            response.raise_for_status()
            return response.json()
    except (httpx.TimeoutException, httpx.ConnectError):
        raise HTTPException(status_code=503, detail="Servicio de reportes no disponible")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Respuesta inválida del servicio de reportes")


@router.get("/stats")
async def stats(user: dict = Depends(require_role(ADMIN_ROLE))):
    return await _get("/stats")


@router.get("/documents/summary")
async def documents_summary(user: dict = Depends(require_role(ADMIN_ROLE))):
    return await _get("/documents/summary")


@router.get("/documents/{document_id}/trace")
async def document_trace(document_id: uuid.UUID, user: dict = Depends(require_role(ADMIN_ROLE))):
    return await _get(f"/documents/{document_id}/trace")