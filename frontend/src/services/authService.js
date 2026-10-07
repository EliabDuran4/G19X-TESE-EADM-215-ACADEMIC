import api from "./api";

export async function login(username, password) {
  const res = await api.post("/auth/login", { username, password });
  localStorage.setItem("access_token", res.data.access_token);

  const payload = JSON.parse(atob(res.data.access_token.split(".")[1]));
  const roles = payload.realm_access?.roles || [];

  localStorage.setItem("roles", JSON.stringify(roles));
  localStorage.setItem("username", payload.preferred_username);

  return roles;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("roles");
  localStorage.removeItem("username");
}

export function getRoles() {
  return JSON.parse(localStorage.getItem("roles") || "[]");
}

export function getUsername() {
  return localStorage.getItem("username") || "";
}

export function isAuthenticated() {
  return !!localStorage.getItem("access_token");
}