const API_BASE = "http://127.0.0.1:5000";

async function apiFetch(endpoint, options = {}) {
  const defaultOptions = {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
  };
  const mergedOptions = { ...defaultOptions, ...options };
  if (options.headers) {
    mergedOptions.headers = { ...defaultOptions.headers, ...options.headers };
  }

  const res = await fetch(`${API_BASE}${endpoint}`, mergedOptions);

  // If session expired or not logged in, redirect to login
  if (res.status === 401) {
    window.location.href = "index.html";
    return;
  }
  return res;
}

async function logout() {
  await apiFetch("/logout", { method: "POST" });
  window.location.href = "index.html";
}

// Show username in navbar if element exists
async function loadNavUser() {
  const el = document.getElementById("nav-username");
  if (!el) return;
  const res = await apiFetch("/me");
  if (res && res.ok) {
    const data = await res.json();
    el.textContent = `👤 ${data.username}`;
  }
}
loadNavUser();
