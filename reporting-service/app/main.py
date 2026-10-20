from fastapi import FastAPI, HTTPException
from app.database import query
from app.telemetry import setup_telemetry

app = FastAPI(title="Reporting Service")
setup_telemetry(app)

def _run(sql: str, params: dict | None = None):
    try:
        return query(sql, params)
    except Exception:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")


@app.get("/health")
def health():
    return {"status": "ok", "service": "reporting-service"}


@app.get("/health/db")
def health_db():
    rows = _run("SELECT COUNT(*) AS total FROM dbo.vw_resumen_documentos")
    return {"status": "ok", "documentos_en_vista": rows[0]["total"]}


@app.get("/stats")
def stats():
    por_categoria_estado = _run(
        "SELECT Categoria, Estado, TotalDocumentos FROM dbo.vw_estadisticas_documentos "
        "ORDER BY Categoria, Estado"
    )
    total_eventos = _run("SELECT COUNT(*) AS total FROM dbo.vw_trazabilidad_documental")[0]["total"]
    totales_estado: dict[str, int] = {}
    for r in por_categoria_estado:
        totales_estado[r["Estado"]] = totales_estado.get(r["Estado"], 0) + r["TotalDocumentos"]
    return {
        "total_documentos": sum(totales_estado.values()),
        "total_eventos": total_eventos,
        "por_estado": totales_estado,
        "por_categoria_estado": por_categoria_estado,
    }


@app.get("/documents/summary")
def documents_summary():
    return _run("SELECT * FROM dbo.vw_resumen_documentos ORDER BY FechaCarga DESC")


@app.get("/documents/{document_id}/trace")
def document_trace(document_id: str):
    return _run(
        "SELECT * FROM dbo.vw_trazabilidad_documental WHERE DocumentoID = :id "
        "ORDER BY FechaEvento DESC, EventoID DESC",
        {"id": document_id},
    )