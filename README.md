# SkillForge AI

AI-powered roadmap-based learning platform built with React, FastAPI, PostgreSQL, and Gemini.

## Features

- Browse 12 expertise categories with animated cards
- 3 roadmap levels per expertise (Beginner, Intermediate, Advanced)
- JWT authentication with persisted login
- AI-generated skill content via Gemini (cached in database)
- 5-question MCQ quizzes with proficiency scoring
- Progress dashboard with Recharts visualizations
- Admin panel for CRUD management and analytics

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React, TypeScript, Vite, TanStack Query, Zustand, Tailwind CSS, Framer Motion, Recharts |
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic, JWT, Passlib |
| Database | PostgreSQL |
| AI | Google Gemini API |
| Deploy | Docker, Docker Compose |

## Quick Start (Docker)

```bash
# Clone and start all services
docker compose up --build

# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

Set your Gemini API key:

```bash
# Create .env in project root
GEMINI_API_KEY=your-key-here
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@skillforge.ai | admin123456 |

## API Endpoints

- `POST /api/auth/register` · `POST /api/auth/login` · `GET /api/auth/me`
- `GET /api/expertise` · `GET /api/roadmaps/{id}` · `GET /api/roadmap/{id}`
- `GET /api/skills/{id}` · `POST /api/topics/complete`
- `POST /api/quiz/generate` · `POST /api/quiz/submit`
- `GET /api/dashboard`
- `POST /api/admin/login` · Admin CRUD at `/api/admin/*`

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access
│   │   ├── models/       # SQLAlchemy models
│   │   └── schemas/      # Pydantic schemas
│   ├── alembic/          # Migrations
│   └── scripts/seed.py   # Seed data
├── frontend/
│   └── src/
│       ├── components/   # UI components
│       ├── pages/        # Route pages
│       ├── services/     # API client
│       └── store/        # Zustand stores
└── docker-compose.yml
```

## Color System

- Primary: `#2563EB` · Secondary: `#7C3AED` · Accent: `#06B6D4`
- Background: `#0F172A` · Surface: `#1E293B`

## License

MIT
