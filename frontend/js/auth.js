const API_BASE = "http://127.0.0.1:5000";

async function loginUser() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const errorEl = document.getElementById("error-msg");
  errorEl.textContent = "";

  if (!email || !password) {
    errorEl.textContent = "Please fill in all fields.";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      window.location.href = "dashboard.html";
    } else {
      errorEl.textContent = data.error;
    }
  } catch (err) {
    errorEl.textContent = "Cannot connect to server. Is Flask running?";
  }
}

async function registerUser() {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const errorEl = document.getElementById("error-msg");
  const successEl = document.getElementById("success-msg");
  errorEl.textContent = "";
  successEl.textContent = "";

  if (!username || !email || !password) {
    errorEl.textContent = "Please fill in all fields.";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      successEl.textContent = "Account created! Redirecting to login...";
      setTimeout(() => (window.location.href = "index.html"), 1500);
    } else {
      errorEl.textContent = data.error;
    }
  } catch (err) {
    errorEl.textContent = "Cannot connect to server. Is Flask running?";
  }
}
