# SkillForge AI

> AI-Powered Roadmap Learning Platform for Developers

SkillForge AI is a full-stack web application that helps aspiring and experienced developers learn technical skills through structured roadmaps, AI-generated learning content, and progress tracking.

Instead of overwhelming users with countless resources, SkillForge AI provides curated learning paths across multiple technical domains such as Frontend Development, Backend Development, DevOps, Data Analytics, Database Engineering, and more.

Users can explore expertise areas without signing up, compare different learning roadmaps based on difficulty levels, and then create an account to begin tracking their learning journey.

---

## Features

### Expertise-Based Learning

Choose from multiple technical domains:

* Frontend Development
* Backend Development
* Database Engineering
* DevOps
* QA Engineering
* Data Analytics
* Data Engineering
* Machine Learning
* Cloud Engineering
* Cybersecurity
* Mobile Development
* System Design

---

### Structured Roadmaps

Each expertise contains three learning paths:

#### Beginner

Perfect for users with little or no prior experience.

#### Intermediate

Focused on building job-ready skills.

#### Advanced

Designed for developers looking to deepen their expertise.

Each roadmap includes:

* Skills
* Topics
* Learning sequence
* Estimated duration

---

### AI-Powered Learning Content

SkillForge AI uses Google's Gemini API to generate:

* Skill overviews
* Core concepts
* Beginner-friendly explanations
* Real-world examples
* Learning summaries

Generated content is cached to reduce API usage and improve performance.

---

### Topic-Based Progress Tracking

Each skill is divided into multiple topics.

Users can:

* Mark topics as completed
* Track skill progress
* Monitor roadmap completion
* Resume learning anytime

---

### Quiz System

Every skill includes a short assessment.

Features:

* 5 AI-generated MCQs
* Multiple-choice answers
* Explanations for correct answers
* Proficiency scoring

Quiz results contribute to overall learning progress.

---

### User Dashboard

Track your learning journey through:

* Roadmap progress
* Completed skills
* Quiz scores
* Recently completed topics
* Learning analytics

---

### Admin Panel

Administrators can manage:

* Expertise categories
* Roadmaps
* Skills
* Topics
* AI prompts
* User progress

---

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* React Router
* TanStack Query
* Zustand
* Tailwind CSS
* Shadcn UI
* Framer Motion
* Recharts

### Backend

* FastAPI
* Python 3.12
* SQLAlchemy
* Alembic
* Pydantic
* JWT Authentication

### Database

* PostgreSQL

### AI

* Google Gemini API

### DevOps

* Docker
* Docker Compose

---

## Architecture

```text
Frontend (React + TypeScript)
            |
            |
            V
Backend API (FastAPI)
            |
            |
    -------------------
    |                 |
    V                 V
PostgreSQL      Gemini API
(Database)      (AI Content)
```

---

## User Flow

### Step 1

Browse expertise categories without authentication.

### Step 2

Select an expertise.

Example:

```text
Frontend Development
```

### Step 3

Choose a roadmap:

```text
Beginner
Intermediate
Advanced
```

### Step 4

Click Start Learning.

### Step 5

Create an account or sign in.

### Step 6

Learn skills and topics.

### Step 7

Complete quizzes and track progress.

---

## Database Design

Core entities:

```text
Users
Expertsise
Roadmaps
Skills
Topics
Skill Contents
Skill Quizzes
Quiz Attempts
User Progress
Admin Users
Prompt Templates
```

---

## Security Features

* Password hashing with bcrypt
* JWT authentication
* Protected routes
* Input validation
* Role-based admin access
* Environment-based configuration

---

## Project Structure

```text
skillforge-ai/

frontend/
│
├── src/
│   ├── components/
│   ├── features/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── store/
│   ├── layouts/
│   ├── routes/
│   └── utils/

backend/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── admin/
│   ├── skills/
│   ├── quizzes/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── database/
│   └── core/
```

---

## Local Development

### Clone Repository

```bash
git clone https://github.com/your-username/skillforge-ai.git

cd skillforge-ai
```

### Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Create `.env`

```env
DATABASE_URL=postgresql://user:password@localhost:5432/skillforge

SECRET_KEY=your-secret-key

GEMINI_API_KEY=your-gemini-api-key
```

Run migrations:

```bash
alembic upgrade head
```

Start server:

```bash
uvicorn app.main:app --reload
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## Future Enhancements

* Personalized roadmap recommendations
* Coding challenges
* Learning streak rewards
* AI mentor assistant
* Skill certificates
* Community discussions
* Learning analytics dashboard
* Roadmap sharing

---

## Why This Project?

SkillForge AI was built to demonstrate:

* Full-Stack Development
* Modern React Architecture
* FastAPI Backend Development
* PostgreSQL Database Design
* Authentication & Authorization
* AI Integration with Gemini
* Dashboard & Analytics Development
* Scalable SaaS Architecture
* Clean UI/UX Design

---

## License

MIT License

---

## Author

Built as a portfolio project to showcase modern full-stack development and AI integration using React, FastAPI, PostgreSQL, and Gemini AI.


MIT
