# Fake News Detection System

A production-style full-stack platform for fake news classification with:
- **Python + FastAPI** backend API
- **React + Vite** dashboard frontend
- **Machine learning pipeline** (TF-IDF + Logistic Regression)
- **JWT authentication**
- **Analytics dashboard** (classification distribution, confidence, scan volume)
- **Model training endpoint** for retraining with uploaded CSV datasets

---

## Architecture

```text
frontend (React/Vite)
  ├── Login/Register UI
  ├── News classification form
  ├── Analytics dashboard (Recharts)
  └── API client (Axios)

backend (FastAPI)
  ├── Auth routes (register/login)
  ├── Prediction routes
  ├── Analytics route
  ├── Training route (CSV upload)
  ├── SQLite persistence (users + predictions)
  └── ML model service (joblib persisted)
```

---

## Features

### 1) Authentication & Access Control
- User registration and login.
- Password hashing with bcrypt.
- Bearer token auth using JWT.
- Protected endpoints for prediction, analytics, and model retraining.

### 2) News Classification
- Classifies user-submitted article title + content as **FAKE** or **REAL**.
- Returns confidence score.
- Stores each prediction event in the database for historical analysis.

### 3) Analytics Dashboard
- Total predictions.
- Fake and real counts.
- Fake news ratio.
- Average confidence.
- Pie chart visualization of classification split.

### 4) Model Training Support
- Upload a CSV file with `text` and `label` columns.
- Retrains model and persists the updated pipeline.
- Returns training metrics such as test accuracy and sample size.

---

## Project Structure

```text
fake-news-detection-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── data/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## Backend Setup (FastAPI)

### Prerequisites
- Python 3.10+
- pip

### Install

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run API

```bash
uvicorn app.main:app --reload --port 8000
```

API docs:
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Frontend Setup (React + Vite)

### Prerequisites
- Node.js 18+
- npm

### Install & Run

```bash
cd frontend
npm install
npm run dev
```

Frontend default URL: `http://localhost:5173`

---

## API Overview

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`

### News
- `POST /api/predict` (auth required)

### Analytics
- `GET /api/analytics` (auth required)

### Training
- `POST /api/train` (auth required, multipart CSV upload)

---

## CSV Training Format

Your training file must include:
- `text` column (combined article text)
- `label` column (`FAKE` or `REAL`)

Example:

```csv
text,label
"Government confirms alien mothership landed in city square",FAKE
"National weather service publishes official rainfall report",REAL
```

---

## Security Notes (Production)

Before production deployment:
- Move secrets to environment variables.
- Use HTTPS and secure cookie/session strategy.
- Replace permissive CORS with explicit origins.
- Add rate limiting and request auditing.
- Add role-based authorization for model training.

---

## Future Enhancements

- Integrate larger curated fake-news datasets.
- Add explainability (top weighted terms / SHAP).
- Add source credibility scoring.
- Add admin panel for model versioning.
- Add CI pipeline with automated API/frontend tests.

---

## License

MIT (see `LICENSE`).
