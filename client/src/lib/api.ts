const csrf = () => document.cookie.split("; ").find((row) => row.startsWith("csrftoken="))?.split("=")[1] || "";
const api = async <T>(path: string, options: RequestInit = {}): Promise<T> => {
  const response = await fetch(path, { credentials: "include", headers: { "Content-Type": "application/json", ...(csrf() ? { "X-CSRFToken": csrf() } : {}), ...(options.headers || {}) }, ...options });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || "تعذر الاتصال بالخادم");
  return body;
};
export type SessionUser = { id: number; username: string; name: string; role: "admin" | "cashier"; role_label: string; branch: string };
export const authApi = { me: () => api<{ user: SessionUser }>("/api/auth/me/"), login: async (username: string, password: string) => { await fetch("/api/auth/csrf/", { credentials: "include" }); return api<{ user: SessionUser }>("/api/auth/login/", { method: "POST", body: JSON.stringify({ username, password }) }); }, logout: () => api<{ ok: boolean }>("/api/auth/logout/", { method: "POST" }) };
export const dashboardApi = { get: () => api<any>("/api/dashboard/"), createTransaction: (data: object) => api<{ ok: boolean; reference: string }>("/api/transactions/", { method: "POST", body: JSON.stringify(data) }) };
