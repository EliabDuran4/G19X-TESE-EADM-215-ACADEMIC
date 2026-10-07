import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authService";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/documents");
    } catch {
      setError("Usuario o contraseña incorrectos");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-card">
        <h1>Observabilidad Documental</h1>
        <p className="subtitle">Inicia sesión para continuar</p>
        <form onSubmit={handleSubmit}>
          <label>Usuario</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          <label>Contraseña</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit" disabled={loading}>{loading ? "Ingresando..." : "Ingresar"}</button>
        </form>
        {error && <div className="login-error">{error}</div>}
      </div>
    </div>
  );
}