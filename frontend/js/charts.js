async function loadDashboard() {
  // Load summary cards
  const summaryRes = await apiFetch("/summary");
  if (!summaryRes) return;
  const summary = await summaryRes.json();

  document.getElementById("total-income").textContent =
    `₹${summary.total_income.toFixed(2)}`;
  document.getElementById("total-expense").textContent =
    `₹${summary.total_expense.toFixed(2)}`;

  const balanceEl = document.getElementById("balance");
  balanceEl.textContent = `₹${summary.balance.toFixed(2)}`;
  balanceEl.style.color = summary.balance >= 0 ? "#27ae60" : "#e74c3c";

  // Load pie chart (category breakdown)
  const catRes = await apiFetch("/chart/category");
  if (!catRes) return;
  const catData = await catRes.json();

  if (catData.length > 0) {
    new Chart(document.getElementById("pieChart"), {
      type: "pie",
      data: {
        labels: catData.map((d) => d.category),
        datasets: [
          {
            data: catData.map((d) => d.total),
            backgroundColor: [
              "#FF6384",
              "#36A2EB",
              "#FFCE56",
              "#4BC0C0",
              "#9966FF",
              "#FF9F40",
              "#C9CBCF",
            ],
          },
        ],
      },
      options: {
        plugins: { legend: { position: "bottom" } },
      },
    });
  } else {
    document.getElementById("pieChart").parentElement.innerHTML +=
      '<p style="color:#999; text-align:center;">No expense data yet</p>';
  }

  // Load bar chart (monthly trend)
  const monthRes = await apiFetch("/chart/monthly");
  if (!monthRes) return;
  const monthData = await monthRes.json();

  new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: {
      labels: monthData.map((d) => d.month),
      datasets: [
        {
          label: "Expenses (₹)",
          data: monthData.map((d) => d.total),
          backgroundColor: "#FF6384",
          borderRadius: 6,
        },
      ],
    },
    options: {
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } },
    },
  });
}

loadDashboard();
