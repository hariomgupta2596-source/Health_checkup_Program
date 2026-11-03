# Health Checkup Program

## Overview

**Health Checkup Program** is a modern, responsive web application built with **Streamlit** that allows users to:
- Register and securely log in.
- Record comprehensive health assessments (vitals, lifestyle, medical history).
- Store data persistently in a **SQLite** database.
- View an interactive dashboard with Plotly visualisations (BMI trend, blood pressure history).
- Generate downloadable PDF health reports (ReportLab).
- Browse educational health guidelines.

The app is intentionally **educational only** – it does **not** provide medical diagnosis.

---

## Project Structure
```
Health_checkup_Program/
│
├─ app.py                     # Entry point – sets up Streamlit config & navigation
├─ requirements.txt           # Python dependencies
├─ README.md                  # This file
│
├─ assets/
│   └─ styles.css             # Custom CSS styling
│
├─ authentication/
│   ├─ __init__.py            # Password hashing utilities (passlib bcrypt)
│   ├─ login.py               # Login page
│   └─ register.py            # Registration page
│
├─ database/
│   ├─ db_connection.py       # SQLAlchemy engine & session helper
│   ├─ db_setup.py            # Table definitions & create_all()
│   └─ init_db.py             # Simple script to initialise the DB
│
├─ modules/
│   ├─ health_checkup.py      # Persist checkup helper
│   ├─ health_analysis.py     # Rule‑based recommendation engine
│   └─ bmi_calculator.py      # (placeholder – future calculations)
│
├─ pages/
│   ├─ __init__.py
│   ├─ home.py                # Landing page
│   ├─ health_checkup.py      # Form page (writes to DB)
│   ├─ dashboard.py           # User dashboard with Plotly charts
│   ├─ reports.py             # PDF report generation & download
│   └─ guidelines.py          # Static health education content
│
├─ utils/
│   ├─ charts.py              # Data loading + Plotly chart helpers
│   └─ pdf_generator.py       # ReportLab PDF creation
│
└─ tests/
    ├─ test_auth.py           # Authentication unit tests
    └─ test_database.py       # DB insert/retrieve tests
```

---

## Setup & Installation
1. **Clone the repository** (or place the source folder in your workspace).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # on Windows
   # or: source venv/bin/activate  # on macOS/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialise the SQLite database** (creates `health_checkup.db` in the project root):
   ```bash
   python -m database.init_db
   ```
5. **Run the application**:
   ```bash
   streamlit run app.py
   ```
   The app will be available at `http://localhost:8501`.

---

## Testing
The project includes a small test suite using **pytest**.
```bash
pytest tests
```
All tests should pass, confirming that:
- Password hashing & verification works.
- Duplicate usernames are rejected.
- Health checkup records are correctly persisted with condition flags.

---

## Docker Deployment (Optional)
You can containerise the app with the provided `Dockerfile`.
```bash
# Build the image
docker build -t health-checkup-program .

# Run the container (exposes Streamlit default port 8501)
docker run -p 8501:8501 health-checkup-program
```
Open `http://localhost:8501` in your browser.

**Dockerfile**
```Dockerfile
# Use an official lightweight Python image
FROM python:3.11-slim

# Set a non‑root user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy only the necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership to the non‑root user
RUN chown -R appuser:appuser .
USER appuser

# Expose Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
```

**.dockerignore** (optional, placed in project root):
```
__pycache__
*.pyc
*.pyo
*.pyd
.env
*.sqlite3
.idea
.git
```

---

## Configuration & Secrets
- The SQLite database file (`health_checkup.db`) is created in the project root and holds all user data.
- Passwords are never stored in plain text – they are hashed with **bcrypt** via Passlib.
- No external API keys or secrets are required for the core functionality.

---

## Future Enhancements
- Add **BMI calculator** module with age‑adjusted categories for children.
- Implement **profile editing** (user details, avatar, etc.).
- Extend **visualisations** (e.g., heart‑rate trends, water intake heatmaps).
- Add **email verification** and password‑reset flow.
- Incorporate **role‑based permissions** for admin dashboards.

---

## License
This project is provided under the **MIT License** – feel free to adapt, improve, and share.
