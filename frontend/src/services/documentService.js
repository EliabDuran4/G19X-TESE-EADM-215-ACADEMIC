import api from "./api";

export async function uploadDocument(file, category) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("category", category);
  const res = await api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function listDocuments() {
  const res = await api.get("/documents/");
  return res.data;
}

export async function getArchive() {
  const res = await api.get("/documents/archive");
  return res.data;
}

export async function reviewDocument(id, new_status, comment) {
  const res = await api.post(`/documents/${id}/review`, { new_status, comment });
  return res.data;
}

export async function decideDocument(id, new_status, comment) {
  const res = await api.post(`/documents/${id}/decide`, { new_status, comment });
  return res.data;
}

export async function deleteDocument(id) {
  const res = await api.delete(`/documents/${id}`);
  return res.data;
}

export async function analyzeDocument(id) {
  const res = await api.post(`/documents/${id}/analyze`);
  return res.data;
}

export async function downloadDocument(id, filename) {
  const res = await api.get(`/documents/${id}/download`, { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}