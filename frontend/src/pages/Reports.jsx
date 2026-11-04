import React, { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import api from "../services/api";
import { getRoles } from "../services/authService";

export default function Reports() {
  const isAdmin = getRoles().includes("admin_documental");
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isAdmin) return;
    api.get("/reports/stats")
      .then((r) => setStats(r.data))
      .catch((e) => setError(
        e.response?.status === 503
          ? "El servicio de reportes no está disponible"
          : "No se pudieron cargar los reportes"
      ));
  }, [isAdmin]);

  if (!isAdmin) return <Navigate to="/documents" replace />;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Legal<span>Tech</span></div>
        <nav>
          <Link to="/documents">Dashboard</Link>
          <Link to="/archive">Documentos</Link>
          <Link className="active" to="/reports">Reportes</Link>
        </nav>
      </aside>

            <div className="rep-main">
        <h2 className="rep-title">Reportes</h2>
        <p className="rep-sub">Resumen del proceso documental</p>

        {error && <div className="rep-error">{error}</div>}
        {!stats && !error && <p>Cargando...</p>}

        {stats && (
          <>
            <div className="rep-cards">
              <div className="rep-card">
                <small>Total de documentos</small>
                <strong>{stats.total_documentos}</strong>
              </div>
              <div className="rep-card">
                <small>Total de eventos</small>
                <strong>{stats.total_eventos}</strong>
              </div>
            </div>

            <div className="rep-grid">
              <div className="rep-panel">
                <h3>Por estado</h3>
                <table className="rep-table">
                  <thead>
                    <tr><th>Estado</th><th style={{ textAlign: "right" }}>Documentos</th></tr>
                  </thead>
                  <tbody>
                    {Object.entries(stats.por_estado).map(([estado, total]) => (
                      <tr key={estado}>
                        <td>
                          <span className={`rep-badge ${estado}`}>{estado}</span>
                          <div className="rep-bar">
                            <span style={{ width: `${(total / (stats.total_documentos || 1)) * 100}%` }} />
                          </div>
                        </td>
                        <td className="num">{total}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="rep-panel">
                <h3>Por categoría y estado</h3>
                <table className="rep-table">
                  <thead>
                    <tr><th>Categoría</th><th>Estado</th><th style={{ textAlign: "right" }}>Docs</th></tr>
                  </thead>
                  <tbody>
                    {stats.por_categoria_estado.map((f) => (
                      <tr key={`${f.Categoria}-${f.Estado}`}>
                        <td>{f.Categoria.replaceAll("_", " ")}</td>
                        <td><span className={`rep-badge ${f.Estado}`}>{f.Estado}</span></td>
                        <td className="num">{f.TotalDocumentos}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}