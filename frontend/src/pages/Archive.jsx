import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { getArchive, reviewDocument, deleteDocument, downloadDocument } from "../services/documentService";
import { logout, getRoles, getUsername } from "../services/authService";

export default function Archive() {
  const [data, setData] = useState({ approved: [], rejected: [] });
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);
  const navigate = useNavigate();

  const roles = getRoles();
  const username = getUsername();
  const isAdmin = roles.includes("admin_documental");
  const isRevisor = roles.includes("revisor_documental");
  const primaryRole = isAdmin ? "admin documental" : isRevisor ? "revisor documental" : "usuario documental";

  const load = async () => {
    setLoading(true);
    try {
      const res = await getArchive();
      setData(res);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAdmin && !isRevisor) {
      navigate("/documents");
      return;
    }
    load();
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handleReopen = async (id) => {
    setBusyId(id);
    try {
      await reviewDocument(id, "en_revision");
      load();
    } catch {
      alert("No se pudo volver a poner en revisión");
    } finally {
      setBusyId(null);
    }
  };

  const handleDelete = async (id, filename) => {
    if (!window.confirm(`¿Eliminar "${filename}"?`)) return;
    setBusyId(id);
    try {
      await deleteDocument(id);
      load();
    } catch {
      alert("No se pudo eliminar");
    } finally {
      setBusyId(null);
    }
  };

  const handleDownload = async (id, filename) => {
    setBusyId(id);
    try {
      await downloadDocument(id, filename);
    } finally {
      setBusyId(null);
    }
  };

  const renderList = (docs, emptyLabel) => {
    if (docs.length === 0) return <div className="empty-state">{emptyLabel}</div>;
    return (
      <table className="docs-table">
        <thead>
          <tr>
            <th>Archivo</th>
            <th>Categoría</th>
            <th>Usuario</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {docs.map((d) => (
            <tr key={d.id}>
              <td>{d.original_filename}</td>
              <td>{d.category}</td>
              <td>{d.uploaded_by}</td>
              <td>{d.uploaded_at ? new Date(d.uploaded_at).toLocaleDateString() : "-"}</td>
              <td>
                <button className="action-btn review" disabled={busyId === d.id} onClick={() => handleDownload(d.id, d.original_filename)}>
                  Descargar
                </button>
                <button className="action-btn correction" disabled={busyId === d.id} onClick={() => handleReopen(d.id)}>
                  Volver a revisión
                </button>
                {isAdmin && (
                  <button className="action-btn delete" disabled={busyId === d.id} onClick={() => handleDelete(d.id, d.original_filename)}>
                    Eliminar
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Legal<span>Tech</span></div>
        <nav>
          <Link to="/documents">Dashboard</Link>
          <Link className="active" to="/archive">Documentos</Link>
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
          {loading ? (
            <div className="loading-state">Cargando...</div>
          ) : (
            <>
              <div className="table-box" style={{ marginBottom: 22 }}>
                <h3>Aprobados ({data.approved.length})</h3>
                {renderList(data.approved, "No hay documentos aprobados.")}
              </div>
              <div className="table-box">
                <h3>Rechazados ({data.rejected.length})</h3>
                {renderList(data.rejected, "No hay documentos rechazados.")}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}