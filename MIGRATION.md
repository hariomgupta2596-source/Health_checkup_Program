# Health Checkup Program — Next.js & FastAPI Architecture

This application has been migrated from Streamlit to a modern decoupled architecture:
- **Frontend:** Next.js (React) — ready for deployment on **Vercel**
- **Backend:** FastAPI (Python) — serving REST API endpoints and reusing existing SQLite DB, SQLAlchemy models, and ReportLab PDF generation

---

## 📁 Project Architecture

```
Health_checkup_Program/
├── backend/
│   ├── main.py              # FastAPI REST endpoints (/api/register, /api/login, /api/checkup, /api/dashboard, /api/reports/...)
│   └── requirements.txt     # Backend dependencies (fastapi, uvicorn, sqlalchemy, etc.)
│
├── frontend/                # Next.js (Vercel-ready)
│   ├── components/          # Reusable UI components (Sidebar, Card, Layout)
│   ├── pages/
│   │   ├── _app.js          # App wrapper and styles
│   │   ├── index.js         # Home page (Hero, quick actions, statistics)
│   │   ├── login.js         # User login
│   │   ├── register.js      # User registration
│   │   ├── healthcheck.js   # Health checkup form & live results
│   │   ├── dashboard.js     # Health dashboard with Plotly charts
│   │   ├── reports.js       # Health PDF reports generator & downloader
│   │   └── guidelines.js    # Tabbed health guidelines & recommendations
│   ├── styles/              # CSS Modules & global styling
│   ├── utils/api.js         # Axios API client configured with auth headers
│   ├── package.json
│   ├── next.config.js
│   └── .env.local           # Local API endpoint: NEXT_PUBLIC_API_URL=http://localhost:8000
│
├── database/                # SQLite connection and schema setup
├── authentication/          # Password hashing and authentication utilities
├── modules/                 # Checkup domain persistence
└── utils/                   # PDF generation utilities
```

---

## 🚀 Running Locally

### 1. Start the FastAPI Backend
Open your terminal at the project root:
```powershell
Set-Location "c:\hariom\project\Health_checkup_Program"
.\venv\Scripts\uvicorn.exe backend.main:app --reload --port 8000
```
The interactive API documentation will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the Next.js Frontend
Open a second terminal window:
```powershell
Set-Location "c:\hariom\project\Health_checkup_Program\frontend"
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your web browser.

---

## ☁️ Deploying to Vercel

1. Push your repository to GitHub, GitLab, or Bitbucket.
2. Go to [Vercel](https://vercel.com/) and click **"Add New Project"**.
3. Import this repository.
4. In the **Configure Project** step:
   - Set **Root Directory** to `frontend`.
   - Under **Environment Variables**, add:
     - `NEXT_PUBLIC_API_URL`: URL of your deployed FastAPI backend (e.g., on Render, Railway, Fly.io, or AWS).
5. Click **Deploy**. Vercel will build and deploy your Next.js application automatically!
