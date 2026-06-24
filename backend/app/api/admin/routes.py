from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.limiter import limiter
from app.database.session import get_db
from app.models import Admin
from app.schemas.auth import AdminLogin, AdminResponse, TokenResponse
from app.schemas.dashboard import AnalyticsResponse, PromptTemplateCreate, PromptTemplateResponse, PromptTemplateUpdate, UserProgressSummary
from app.schemas.roadmap import (
    ExpertiseCreate,
    ExpertiseResponse,
    ExpertiseUpdate,
    RoadmapCreate,
    RoadmapSummary,
    RoadmapUpdate,
    SkillCreate,
    SkillResponse,
    SkillSummary,
    SkillUpdate,
    TopicCreate,
    TopicResponse,
    TopicUpdate,
)
from app.services.admin_auth_service import AdminAuthService
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def admin_login(request: Request, data: AdminLogin, db: Session = Depends(get_db)):
    _, token = AdminAuthService(db).login(data)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=AdminResponse)
def admin_me(current_admin: Admin = Depends(get_current_admin)):
    return AdminResponse.model_validate(current_admin)


# Expertise
@router.get("/expertise", response_model=list[ExpertiseResponse])
def admin_list_expertise(db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).list_expertise()


@router.post("/expertise", response_model=ExpertiseResponse)
def admin_create_expertise(data: ExpertiseCreate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).create_expertise(data)


@router.put("/expertise/{expertise_id}", response_model=ExpertiseResponse)
def admin_update_expertise(expertise_id: int, data: ExpertiseUpdate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).update_expertise(expertise_id, data)


@router.delete("/expertise/{expertise_id}")
def admin_delete_expertise(expertise_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    AdminService(db).delete_expertise(expertise_id)
    return {"message": "Expertise deleted"}


# Roadmaps
@router.get("/roadmaps", response_model=list[RoadmapSummary])
def admin_list_roadmaps(expertise_id: int | None = None, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).list_roadmaps(expertise_id)


@router.post("/roadmaps", response_model=RoadmapSummary)
def admin_create_roadmap(data: RoadmapCreate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).create_roadmap(data)


@router.put("/roadmaps/{roadmap_id}", response_model=RoadmapSummary)
def admin_update_roadmap(roadmap_id: int, data: RoadmapUpdate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).update_roadmap(roadmap_id, data)


@router.delete("/roadmaps/{roadmap_id}")
def admin_delete_roadmap(roadmap_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    AdminService(db).delete_roadmap(roadmap_id)
    return {"message": "Roadmap deleted"}


# Skills
@router.get("/roadmaps/{roadmap_id}/skills", response_model=list[SkillSummary])
def admin_list_skills(roadmap_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).list_skills(roadmap_id)


@router.post("/skills", response_model=SkillResponse)
def admin_create_skill(data: SkillCreate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).create_skill(data)


@router.put("/skills/{skill_id}", response_model=SkillResponse)
def admin_update_skill(skill_id: int, data: SkillUpdate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).update_skill(skill_id, data)


@router.delete("/skills/{skill_id}")
def admin_delete_skill(skill_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    AdminService(db).delete_skill(skill_id)
    return {"message": "Skill deleted"}


# Topics
@router.get("/skills/{skill_id}/topics", response_model=list[TopicResponse])
def admin_list_topics(skill_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).list_topics(skill_id)


@router.post("/topics", response_model=TopicResponse)
def admin_create_topic(data: TopicCreate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).create_topic(data)


@router.put("/topics/{topic_id}", response_model=TopicResponse)
def admin_update_topic(topic_id: int, data: TopicUpdate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).update_topic(topic_id, data)


@router.delete("/topics/{topic_id}")
def admin_delete_topic(topic_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    AdminService(db).delete_topic(topic_id)
    return {"message": "Topic deleted"}


# Prompts
@router.get("/prompts", response_model=list[PromptTemplateResponse])
def admin_list_prompts(db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).list_prompts()


@router.post("/prompts", response_model=PromptTemplateResponse)
def admin_create_prompt(data: PromptTemplateCreate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).create_prompt(data)


@router.put("/prompts/{prompt_id}", response_model=PromptTemplateResponse)
def admin_update_prompt(prompt_id: int, data: PromptTemplateUpdate, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).update_prompt(prompt_id, data)


@router.delete("/prompts/{prompt_id}")
def admin_delete_prompt(prompt_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    AdminService(db).delete_prompt(prompt_id)
    return {"message": "Prompt deleted"}


@router.delete("/cache/skills/{skill_id}")
def admin_clear_skill_cache(skill_id: int, db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    AdminService(db).clear_skill_cache(skill_id)
    return {"message": "Skill cache cleared"}


# Users & analytics
@router.get("/users", response_model=list[UserProgressSummary])
def admin_list_users(db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).list_users()


@router.get("/analytics", response_model=AnalyticsResponse)
def admin_analytics(db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return AdminService(db).get_analytics()
