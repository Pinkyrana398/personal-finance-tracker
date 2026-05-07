# 💰 Personal Finance Tracker

A full-stack web application to track income and expenses, visualize spending patterns, and manage monthly budgets — built with Flask, PostgreSQL, and Chart.js.

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)

---

## 🌟 Features

- 🔐 User Authentication — Register, Login, Logout with bcrypt password hashing
- 💸 Transaction Management — Add, view, and delete income/expense transactions
- 🏷️ Category-wise Tracking — Food, Transport, Bills, Entertainment, and more
- 📊 Interactive Dashboard — Pie chart (spending by category) and Bar chart (monthly trend)
- 💰 Summary Cards — Total income, total expense, and current balance at a glance
- 📱 Responsive Design — Works on desktop and mobile

---

## 🛠️ Tech Stack

| Layer    | Technology                                    |
| -------- | --------------------------------------------- |
| Frontend | HTML5, CSS3, Vanilla JavaScript, Chart.js     |
| Backend  | Python 3, Flask, Flask-SQLAlchemy, Flask-CORS |
| Database | PostgreSQL                                    |
| Auth     | bcrypt password hashing, Flask sessions       |
| Tools    | Git, pgAdmin 4, VS Code, Postman              |

---

## 📁 Project Structure

```
personal-finance-tracker/
│
├── backend/
│   ├── app.py                  # Flask app entry point
│   ├── config.py               # Configuration and DB connection
│   ├── extensions.py           # SQLAlchemy instance
│   ├── requirements.txt        # Python dependencies
│   └── routes/
│       ├── auth_routes.py      # Register, Login, Logout APIs
│       └── transaction_routes.py  # Transaction CRUD APIs
│
├── frontend/
│   ├── index.html              # Login page
│   ├── register.html           # Register page
│   ├── dashboard.html          # Dashboard with charts
│   ├── transactions.html       # Transactions table
│   ├── css/
│   │   ├── style.css           # Global styles
│   │   ├── auth.css            # Auth page styles
│   │   └── dashboard.css       # Dashboard styles
│   └── js/
│       ├── api.js              # Centralized fetch helper
│       ├── auth.js             # Login/Register logic
│       ├── transactions.js     # Transaction operations
│       └── charts.js           # Chart.js rendering
│
├── database/
│   └── schema.sql              # PostgreSQL table definitions
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL 14+
- pgAdmin 4

### 1. Clone the repository

```bash
git clone https://github.com/Pinkyrana398/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Set up the database

- Open pgAdmin 4 and create a database named `finance_tracker`
- Run `database/schema.sql` in the Query Tool

### 3. Set up the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 4. Configure environment

Create `backend/config.py` with your PostgreSQL credentials.
Refer to the config template in the Getting Started section above.

### 5. Start the backend

```bash
python app.py
# Flask runs at http://127.0.0.1:5000
```

### 6. Start the frontend

- Open `frontend/index.html` with **Live Server** in VS Code
- Website runs at `http://127.0.0.1:5500`

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint    | Description                |
| ------ | ----------- | -------------------------- |
| POST   | `/register` | Create new user account    |
| POST   | `/login`    | Login and create session   |
| POST   | `/logout`   | Clear session              |
| GET    | `/me`       | Get current logged-in user |

### Transactions

| Method | Endpoint             | Description                              |
| ------ | -------------------- | ---------------------------------------- |
| POST   | `/transactions`      | Add new transaction                      |
| GET    | `/transactions`      | Get all transactions for user            |
| DELETE | `/transactions/<id>` | Delete a transaction                     |
| GET    | `/summary`           | Get income/expense/balance totals        |
| GET    | `/chart/category`    | Get category-wise expense totals         |
| GET    | `/chart/monthly`     | Get monthly expense data (last 6 months) |

---

## 🗄️ Database Schema

```sql
users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    type VARCHAR(10) CHECK (type IN ('income', 'expense')),
    category VARCHAR(50),
    amount DECIMAL(10,2),
    note TEXT,
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## 📸 Screenshots

_(Screenshots will be added soon)_

---

## 🔮 Upcoming Features

- [ ] Filter transactions by date, category, type
- [ ] Monthly budget setting with warnings
- [ ] Export transactions to CSV
- [ ] JWT-based authentication
- [ ] Deploy on Render.com

---

## 👨‍💻 Author

**Pinky Rana**

- GitHub: [@Pinkyrana398](https://github.com/Pinkyrana398)
- LinkedIn: [Pinky Rana](https://www.linkedin.com/in/pinky-rana-7b08b3324/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
