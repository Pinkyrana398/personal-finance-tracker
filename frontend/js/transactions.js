document.getElementById("date").valueAsDate = new Date();

async function loadTransactions() {
  const res = await apiFetch("/transactions");
  if (!res) return;

  const data = await res.json();
  const tbody = document.getElementById("transaction-body");

  if (data.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align:center; color:#999;">No transactions yet. Add one above!</td></tr>';
    return;
  }

  tbody.innerHTML = "";
  data.forEach((t) => {
    const row = document.createElement("tr");
    row.className = t.type === "income" ? "income-row" : "expense-row";
    const sign = t.type === "income" ? "+" : "-";
    row.innerHTML = `
            <td>${t.date}</td>
            <td><span class="badge badge-${t.type}">${t.type}</span></td>
            <td>${t.category}</td>
            <td class="${t.type}-amount">${sign}₹${t.amount.toFixed(2)}</td>
            <td>${t.note || "—"}</td>
            <td><button class="btn-delete" onclick="deleteTransaction(${t.id})">🗑️ Delete</button></td>
        `;
    tbody.appendChild(row);
  });
}

async function addTransaction() {
  const errorEl = document.getElementById("form-error");
  errorEl.textContent = "";

  const amount = parseFloat(document.getElementById("amount").value);
  const date = document.getElementById("date").value;

  if (!amount || amount <= 0) {
    errorEl.textContent = "Please enter a valid amount.";
    return;
  }
  if (!date) {
    errorEl.textContent = "Please select a date.";
    return;
  }

  const payload = {
    type: document.getElementById("type").value,
    category: document.getElementById("category").value,
    amount: amount,
    date: date,
    note: document.getElementById("note").value.trim(),
  };

  const res = await apiFetch("/transactions", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  if (res && res.ok) {
    // Clear form
    document.getElementById("amount").value = "";
    document.getElementById("note").value = "";
    document.getElementById("date").valueAsDate = new Date();
    loadTransactions();
  } else if (res) {
    const data = await res.json();
    errorEl.textContent = data.error || "Failed to add transaction.";
  }
}

async function deleteTransaction(id) {
  if (!confirm("Are you sure you want to delete this transaction?")) return;

  const res = await apiFetch(`/transactions/${id}`, { method: "DELETE" });
  if (res && res.ok) {
    loadTransactions();
  }
}

// Load transactions when page opens
loadTransactions();
