import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Documents from "./pages/Documents";
import Archive from "./pages/Archive";
import { isAuthenticated } from "./services/authService";

function Protected({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/documents"
          element={
            <Protected>
              <Documents />
            </Protected>
          }
        />
        <Route
          path="/archive"
          element={
            <Protected>
              <Archive />
            </Protected>
          }
        />
        <Route path="*" element={<Navigate to="/documents" replace />} />
      </Routes>
    </BrowserRouter>
  );
}