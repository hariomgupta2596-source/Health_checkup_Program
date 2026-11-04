# 🏥 Health Checkup Program

A full-stack, responsive healthcare monitoring web application designed for modern web deployment.

- **Frontend:** Built with **Next.js (React)**, styled with modern CSS Modules, fully optimized for deployment on **Vercel**.
- **Backend:** High-performance **FastAPI (Python)** REST API with CORS support, persistent **SQLite** database via SQLAlchemy 2.0, secure native **bcrypt** authentication, and **ReportLab** PDF generation.

---

## 🌟 Key Features

- **🔐 Secure Authentication:** User registration and login powered by native bcrypt hashing and clean credential verification.
- **📋 Health Assessment Form:** Input comprehensive vitals (height, weight, BP, pulse, temp), lifestyle habits (sleep, exercise, hydration with live sliders), and pre-existing medical conditions.
- **📊 Interactive Dashboard:** Instant metric calculations (BMI category, vitals status) alongside interactive Plotly health trend charts.
- **💡 Personalized Recommendations:** Rule-based health and lifestyle advisory tailored to assessment metrics.
- **📄 PDF Reports:** Downloadable, printable health summary reports generated server-side.
- **📚 Evidence-Based Guidelines:** 5-category health and wellness education covering Nutrition, Exercise, Sleep, Stress, and Disease Prevention.

---

## 📁 Clean Architecture

```
Health_checkup_Program/
├── backend/
│   ├── main.py              # FastAPI REST endpoints & CORS configuration
│   └── requirements.txt     # Python backend dependencies
│
├── frontend/                # Next.js Application (Vercel-ready)
│   ├── components/          # Reusable UI components (Sidebar, Card, Layout)
│   ├── pages/               # Application routes
│   │   ├── _app.js          # Global app wrapper
│   │   ├── index.js         # Landing page with stats & quick actions
│   │   ├── login.js         # User login
│   │   ├── register.js      # User registration
│   │   ├── healthcheck.js   # Assessment questionnaire
│   │   ├── dashboard.js     # Health dashboard with Plotly charts
│   │   ├── reports.js       # PDF report generator & downloader
│   │   └── guidelines.js    # Evidence-based health guidelines
│   ├── styles/              # CSS Modules & global variables
│   ├── utils/api.js         # Axios API client configured with auth headers
│   ├── package.json
│   └── next.config.js
│
├── database/                # SQLite connection and schema definitions
├── authentication/          # Secure bcrypt password hashing utilities
├── modules/                 # Checkup persistence and advisory engine
├── utils/                   # ReportLab PDF generation utilities
├── tests/                   # Pytest test suite (auth, database, and API)
├── requirements.txt         # Root Python requirements
└── LICENSE
```

---

## 🚀 Getting Started

### 1. Backend Setup (FastAPI)
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start the API server
uvicorn backend.main:app --reload --port 8000
```
Interactive API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Frontend Setup (Next.js)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## ☁️ Deployment

### Frontend (Vercel)
1. Push repository to GitHub.
2. In [Vercel](https://vercel.com/), select **Add New Project** and import this repository.
3. Set **Root Directory** to `frontend`.
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g., `https://your-backend.onrender.com`).
5. Click **Deploy**.

### Backend (Render / Railway / Fly.io)
Deploy as a Python Web Service:
- **Build Command:** `pip install -r backend/requirements.txt`
- **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

---

## 🧪 Testing

Run automated tests using pytest:
```bash
pytest
```

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
