/** Client-side auth helpers — tokens live in localStorage and are sent as Bearer headers. */
const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export function getAccessToken(): string | null {
  // Guard for SSR — localStorage is only available in the browser
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setTokens(accessToken: string, refreshToken: string): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export type UserProfile = {
  id: string;
  email: string;
  created_at: string;
};

export async function login(
  email: string,
  password: string,
): Promise<{ access_token: string; refresh_token: string }> {
  // Proxies to POST /auth/login — Supabase returns JWT tokens on success
  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error ?? "Login failed");
  }

  return data;
}

export async function signup(
  email: string,
  password: string,
): Promise<void> {
  // Proxies to POST /auth/signup — creates the user in Supabase Auth
  const res = await fetch("/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error ?? "Signup failed");
  }
}

export async function logout(): Promise<void> {
  const token = getAccessToken();
  if (!token) return;

  // Invalidate the session server-side, then wipe local tokens
  await fetch("/auth/logout", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });

  clearTokens();
}

export async function fetchProfile(): Promise<UserProfile> {
  const token = getAccessToken();
  if (!token) {
    throw new Error("Not authenticated");
  }

  // GET /protected/profile — also acts as a session validity check
  const res = await fetch("/protected/profile", {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await res.json();

  if (!res.ok) {
    // Token is missing, expired, or revoked — clear stale credentials
    clearTokens();
    throw new Error(data.error ?? "Session expired");
  }

  return data;
}

export type DashboardData = {
  message: string;
  user_id: string;
};

export async function fetchDashboard(): Promise<DashboardData> {
  const token = getAccessToken();
  if (!token) {
    throw new Error("Not authenticated");
  }

  // GET /protected/dashboard — personalized greeting from the API
  const res = await fetch("/protected/dashboard", {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await res.json();

  if (!res.ok) {
    clearTokens();
    throw new Error(data.error ?? "Session expired");
  }

  return data;
}
