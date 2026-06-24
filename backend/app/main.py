from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.admin.routes import router as admin_router
from app.api.auth.routes import router as auth_router
from app.api.dashboard.routes import router as dashboard_router
from app.api.quizzes.routes import router as quiz_router
from app.api.roadmaps.routes import router as roadmap_router
from app.api.skills.routes import router as skill_router
from app.core.config import get_settings
from app.core.limiter import limiter

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title="SkillForge AI",
        description="AI-powered roadmap-based learning platform",
        version="1.0.0",
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/api")
    app.include_router(roadmap_router, prefix="/api")
    app.include_router(skill_router, prefix="/api")
    app.include_router(quiz_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")
    app.include_router(admin_router, prefix="/api")

    @app.get("/health")
    @limiter.limit("60/minute")
    def health(request: Request):
        return {"status": "healthy", "service": "skillforge-ai"}

    return app


app = create_app()
