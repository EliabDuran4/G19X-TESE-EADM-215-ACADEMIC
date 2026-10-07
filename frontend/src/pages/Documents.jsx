import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { uploadDocument, listDocuments } from "../services/documentService";
import { logout, getRoles, getUsername } from "../services/authService";
import DocumentRow from "../components/DocumentRow";

const CATEGORIES = [
  { value: "contratos_corporativo", label: "Contratos y Corporativo" },
  { value: "litigioso", label: "Litigioso" },
  { value: "regulatorio_compliance", label: "Regulatorio / Compliance" },
  { value: "propiedad_intelectual", label: "Propiedad Intelectual" },
];

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState(CATEGORIES[0].value);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const roles = getRoles();
  const username = getUsername();
  const isAdmin = roles.includes("admin_documental");
  const primaryRole = isAdmin
    ? "admin documental"
    : roles.includes("revisor_documental")
    ? "revisor documental"
    : "usuario documental";

  const load = async () => {
    setLoading(true);
    try {
      const data = await listDocuments();
      setDocs(data.documents || []);
    } catch {
      setError("No se pudieron cargar los documentos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Selecciona un archivo primero");
      return;
    }
    setUploading(true);
    setError("");
    setMessage("");
    try {
      await uploadDocument(file, category);
      setMessage("Documento cargado exitosamente");
      setFile(null);
      e.target.reset();
      load();
    } catch {
      setError("Error al subir el documento (verifica formato .pdf, .docx, .doc)");
    } finally {
      setUploading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const stats = {
    total: docs.length,
    recibido: docs.filter((d) => d.status === "recibido").length,
    en_revision: docs.filter((d) => d.status === "en_revision").length,
    revisado: docs.filter((d) => d.status === "revisado").length,
    aprobado: docs.filter((d) => d.status === "aprobado").length,
    rechazado: docs.filter((d) => d.status === "rechazado").length,
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Legal<span>Tech</span></div>
        <nav>
          <Link className="active" to="/documents">Dashboard</Link>
          <Link to="/archive">Documentos</Link>
        </nav>
      </aside>

      <div className="main-col">
        <header className="topbar">
          <div />
          <div className="user-box">
            <div className="user-info">
              <div className="uname">{username}</div>
              <div className="urole">{primaryRole}</div>
            </div>
            <div className="avatar">{username ? username[0].toUpperCase() : "U"}</div>
            <button className="logout-btn" onClick={handleLogout}>Salir</button>
          </div>
        </header>

        <div className="content">
          {isAdmin && (
            <div className="upload-box" style={{ borderLeft: "4px solid #1d4ed8" }}>
              <h3>Panel de Administración</h3>
              <p style={{ fontSize: 13, color: "#64748b" }}>
                Como administrador puedes aprobar, rechazar y eliminar documentos.
              </p>
            </div>
          )}

          <div className="stats-grid">
            <div className="stat-card total"><div className="value">{stats.total}</div><div className="label">Total</div></div>
            <div className="stat-card recibido"><div className="value">{stats.recibido}</div><div className="label">Recibidos</div></div>
            <div className="stat-card en_revision"><div className="value">{stats.en_revision}</div><div className="label">En revisión</div></div>
            <div className="stat-card revisado"><div className="value">{stats.revisado}</div><div className="label">Revisados</div></div>
            <div className="stat-card aprobado"><div className="value">{stats.aprobado}</div><div className="label">Aprobados</div></div>
            <div className="stat-card rechazado"><div className="value">{stats.rechazado}</div><div className="label">Rechazados</div></div>
          </div>

          <div className="upload-box">
            <h3>Subir documento</h3>
            <form className="upload-form" onSubmit={handleUpload}>
              <input type="file" accept=".pdf,.docx,.doc" onChange={(e) => setFile(e.target.files[0])} />
              <select value={category} onChange={(e) => setCategory(e.target.value)}>
                {CATEGORIES.map((c) => (
                  <option key={c.value} value={c.value}>{c.label}</option>
                ))}
              </select>
              <button type="submit" disabled={uploading}>{uploading ? "Subiendo..." : "Subir"}</button>
            </form>
            {message && <div className="msg-success">{message}</div>}
            {error && <div className="msg-error">{error}</div>}
          </div>

          <div className="table-box">
            <h3>Documentos ({docs.length})</h3>
            {loading ? (
              <div className="loading-state">Cargando documentos...</div>
            ) : docs.length === 0 ? (
              <div className="empty-state">No hay documentos cargados todavía.</div>
            ) : (
              <table className="docs-table">
                <thead>
                  <tr>
                    <th>Archivo</th>
                    <th>Categoría</th>
                    <th>Estado</th>
                    <th>Usuario</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {docs.map((d) => (
                    <DocumentRow key={d.id} doc={d} onUpdate={load} />
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}