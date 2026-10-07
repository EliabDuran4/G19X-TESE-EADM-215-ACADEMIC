import React, { useState } from "react";
import {
  reviewDocument,
  decideDocument,
  deleteDocument,
  downloadDocument,
  analyzeDocument,
} from "../services/documentService";
import { getRoles } from "../services/authService";

const CATEGORY_LABEL = {
  contratos_corporativo: "Contratos y Corporativo",
  litigioso: "Litigioso",
  regulatorio_compliance: "Regulatorio / Compliance",
  propiedad_intelectual: "Propiedad Intelectual",
};

const AI_WARNING = "El análisis de IA es una herramienta de apoyo y requiere validación humana.";

export default function DocumentRow({ doc, onUpdate }) {
  const [comment, setComment] = useState("");
  const [busy, setBusy] = useState(false);
  const [aiBusy, setAiBusy] = useState(false);
  const [aiOpen, setAiOpen] = useState(false);
  const [aiResult, setAiResult] = useState("");
  const [aiError, setAiError] = useState("");
  const roles = getRoles();
  const isRevisor = roles.includes("revisor_documental");
  const isAdmin = roles.includes("admin_documental");
  const canDownload = isRevisor || isAdmin;
  const canAnalyze = isRevisor || isAdmin;

  const act = async (fn, status) => {
    setBusy(true);
    try {
      await fn(doc.id, status, comment || undefined);
      setComment("");
      onUpdate();
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`¿Eliminar "${doc.original_filename}"? Esta acción no se puede deshacer.`)) return;
    setBusy(true);
    try {
      await deleteDocument(doc.id);
      onUpdate();
    } catch {
      alert("No se pudo eliminar el documento");
    } finally {
      setBusy(false);
    }
  };

  const handleDownload = async () => {
    setBusy(true);
    try {
      await downloadDocument(doc.id, doc.original_filename);
    } catch {
      alert("No se pudo descargar el documento");
    } finally {
      setBusy(false);
    }
  };

  const handleAnalyze = async () => {
    if (aiBusy) return;
    setAiBusy(true);
    setAiError("");
    setAiResult("");
    setAiOpen(true);
    try {
      const data = await analyzeDocument(doc.id);
      setAiResult(data.ai_analysis || "");
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setAiError(
        typeof detail === "string"
          ? detail
          : "No se pudo generar el análisis de IA."
      );
    } finally {
      setAiBusy(false);
    }
  };

  const showRevisorActions = isRevisor && (doc.status === "recibido" || doc.status === "en_revision");
  const showAdminActions = isAdmin && doc.status === "revisado";
  const showCommentInput = showRevisorActions || showAdminActions;

  return (
    <>
      <tr>
        <td>{doc.original_filename}</td>
        <td>{CATEGORY_LABEL[doc.category] || doc.category}</td>
        <td><span className={`badge badge-${doc.status}`}>{doc.status.replace("_", " ")}</span></td>
        <td>{doc.uploaded_by}</td>
        <td>{doc.uploaded_at ? new Date(doc.uploaded_at).toLocaleDateString() : "-"}</td>
        <td>
          {showCommentInput && (
            <input
              className="action-btn comment-input"
              placeholder="Comentario"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              disabled={busy}
            />
          )}

          {canDownload && (
            <button className="action-btn review" disabled={busy} onClick={handleDownload}>
              Descargar
            </button>
          )}

          {canAnalyze && (
            <button
              className="action-btn"
              style={{ background: "#7c3aed" }}
              disabled={busy || aiBusy}
              onClick={handleAnalyze}
            >
              {aiBusy ? "Analizando..." : "Analizar con IA"}
            </button>
          )}

          {isRevisor && doc.status === "recibido" && (
            <button className="action-btn review" disabled={busy} onClick={() => act(reviewDocument, "en_revision")}>
              Iniciar revisión
            </button>
          )}

          {isRevisor && doc.status === "en_revision" && (
            <>
              <button className="action-btn review" disabled={busy} onClick={() => act(reviewDocument, "revisado")}>
                Revisado
              </button>
              <button className="action-btn correction" disabled={busy} onClick={() => act(reviewDocument, "correccion")}>
                Corrección
              </button>
            </>
          )}

          {isAdmin && doc.status === "revisado" && (
            <>
              <button className="action-btn approve" disabled={busy} onClick={() => act(decideDocument, "aprobado")}>
                Aprobar
              </button>
              <button className="action-btn reject" disabled={busy} onClick={() => act(decideDocument, "rechazado")}>
                Rechazar
              </button>
            </>
          )}

          {isAdmin && (
            <button className="action-btn delete" disabled={busy} onClick={handleDelete}>
              Eliminar
            </button>
          )}

          {!showRevisorActions && !showAdminActions && !isAdmin && !canDownload && "-"}
        </td>
      </tr>

      {canAnalyze && aiOpen && (
        <tr>
          <td colSpan={6} style={{ background: "#faf5ff", borderLeft: "4px solid #7c3aed" }}>
            <div style={{ fontWeight: 600, fontSize: 13, marginBottom: 6 }}>
              Análisis de IA: {doc.original_filename}
            </div>
            <div
              style={{
                background: "#fef3c7",
                color: "#92400e",
                padding: "6px 10px",
                borderRadius: 6,
                fontSize: 12,
                marginBottom: 8,
              }}
            >
              {AI_WARNING}
            </div>
            {aiBusy && <div className="loading-state" style={{ padding: 12 }}>Analizando...</div>}
            {aiError && <div className="msg-error">{aiError}</div>}
            {aiResult && (
              <div style={{ whiteSpace: "pre-wrap", fontSize: 13, lineHeight: 1.5 }}>
                {aiResult}
              </div>
            )}
            {!aiBusy && (
              <button
                className="action-btn review"
                style={{ marginTop: 8 }}
                onClick={() => setAiOpen(false)}
              >
                Cerrar
              </button>
            )}
          </td>
        </tr>
      )}
    </>
  );
}