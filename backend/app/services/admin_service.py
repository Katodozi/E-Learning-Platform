from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import Expertise, PromptTemplate, Roadmap, RoadmapLevel, Skill, Topic, User
from app.repositories.admin_repository import AdminRepository
from app.repositories.progress_repository import PromptTemplateRepository, SkillContentRepository, SkillQuizRepository
from app.repositories.roadmap_repository import ExpertiseRepository, RoadmapRepository, SkillRepository, TopicRepository
from app.repositories.user_repository import UserRepository
from app.schemas.dashboard import AnalyticsResponse, PromptTemplateCreate, PromptTemplateResponse, PromptTemplateUpdate, UserProgressSummary
from app.schemas.roadmap import (
    ExpertiseCreate,
    ExpertiseResponse,
    ExpertiseUpdate,
    RoadmapCreate,
    RoadmapDetail,
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


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.expertise_repo = ExpertiseRepository(db)
        self.roadmap_repo = RoadmapRepository(db)
        self.skill_repo = SkillRepository(db)
        self.topic_repo = TopicRepository(db)
        self.prompt_repo = PromptTemplateRepository(db)
        self.user_repo = UserRepository(db)
        self.content_repo = SkillContentRepository(db)
        self.quiz_repo = SkillQuizRepository(db)
        self.admin_repo = AdminRepository(db)

    # Expertise CRUD
    def list_expertise(self) -> list[ExpertiseResponse]:
        return [ExpertiseResponse.model_validate(e) for e in self.expertise_repo.get_all_ordered()]

    def create_expertise(self, data: ExpertiseCreate) -> ExpertiseResponse:
        if self.expertise_repo.get_by_slug(data.slug):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already exists")
        expertise = Expertise(**data.model_dump())
        return ExpertiseResponse.model_validate(self.expertise_repo.create(expertise))

    def update_expertise(self, expertise_id: int, data: ExpertiseUpdate) -> ExpertiseResponse:
        expertise = self.expertise_repo.get_by_id(expertise_id)
        if not expertise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expertise not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(expertise, key, value)
        return ExpertiseResponse.model_validate(self.expertise_repo.update(expertise))

    def delete_expertise(self, expertise_id: int) -> None:
        expertise = self.expertise_repo.get_by_id(expertise_id)
        if not expertise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expertise not found")
        self.expertise_repo.delete(expertise)

    # Roadmap CRUD
    def list_roadmaps(self, expertise_id: int | None = None) -> list[RoadmapSummary]:
        if expertise_id:
            roadmaps = self.roadmap_repo.get_by_expertise(expertise_id)
        else:
            roadmaps = self.roadmap_repo.get_all(limit=1000)
        return [
            RoadmapSummary(
                id=r.id,
                title=r.title,
                level=r.level.value if hasattr(r.level, "value") else r.level,
                description=r.description,
                estimated_duration=r.estimated_duration,
                skill_count=len(r.skills) if hasattr(r, "skills") and r.skills else 0,
            )
            for r in roadmaps
        ]

    def create_roadmap(self, data: RoadmapCreate) -> RoadmapSummary:
        expertise = self.expertise_repo.get_by_id(data.expertise_id)
        if not expertise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expertise not found")
        roadmap = Roadmap(
            expertise_id=data.expertise_id,
            title=data.title,
            level=RoadmapLevel(data.level),
            description=data.description,
            estimated_duration=data.estimated_duration,
        )
        roadmap = self.roadmap_repo.create(roadmap)
        return RoadmapSummary(
            id=roadmap.id,
            title=roadmap.title,
            level=roadmap.level.value,
            description=roadmap.description,
            estimated_duration=roadmap.estimated_duration,
            skill_count=0,
        )

    def update_roadmap(self, roadmap_id: int, data: RoadmapUpdate) -> RoadmapSummary:
        roadmap = self.roadmap_repo.get_by_id(roadmap_id)
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
        updates = data.model_dump(exclude_unset=True)
        if "level" in updates:
            updates["level"] = RoadmapLevel(updates["level"])
        for key, value in updates.items():
            setattr(roadmap, key, value)
        roadmap = self.roadmap_repo.update(roadmap)
        return RoadmapSummary(
            id=roadmap.id,
            title=roadmap.title,
            level=roadmap.level.value,
            description=roadmap.description,
            estimated_duration=roadmap.estimated_duration,
            skill_count=len(roadmap.skills) if roadmap.skills else 0,
        )

    def delete_roadmap(self, roadmap_id: int) -> None:
        roadmap = self.roadmap_repo.get_by_id(roadmap_id)
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
        self.roadmap_repo.delete(roadmap)

    # Skill CRUD
    def list_skills(self, roadmap_id: int) -> list[SkillSummary]:
        roadmap = self.roadmap_repo.get_with_skills(roadmap_id)
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
        return [
            SkillSummary(
                id=s.id,
                name=s.name,
                description=s.description,
                order_index=s.order_index,
                topic_count=len(s.topics),
            )
            for s in roadmap.skills
        ]

    def create_skill(self, data: SkillCreate) -> SkillResponse:
        roadmap = self.roadmap_repo.get_by_id(data.roadmap_id)
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
        skill = Skill(**data.model_dump())
        skill = self.skill_repo.create(skill)
        return SkillResponse.model_validate(skill)

    def update_skill(self, skill_id: int, data: SkillUpdate) -> SkillResponse:
        skill = self.skill_repo.get_by_id(skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(skill, key, value)
        return SkillResponse.model_validate(self.skill_repo.update(skill))

    def delete_skill(self, skill_id: int) -> None:
        skill = self.skill_repo.get_by_id(skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        self.skill_repo.delete(skill)

    # Topic CRUD
    def list_topics(self, skill_id: int) -> list[TopicResponse]:
        topics = self.topic_repo.get_by_skill(skill_id)
        return [TopicResponse.model_validate(t) for t in topics]

    def create_topic(self, data: TopicCreate) -> TopicResponse:
        skill = self.skill_repo.get_by_id(data.skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        topic = Topic(**data.model_dump())
        return TopicResponse.model_validate(self.topic_repo.create(topic))

    def update_topic(self, topic_id: int, data: TopicUpdate) -> TopicResponse:
        topic = self.topic_repo.get_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(topic, key, value)
        return TopicResponse.model_validate(self.topic_repo.update(topic))

    def delete_topic(self, topic_id: int) -> None:
        topic = self.topic_repo.get_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        self.topic_repo.delete(topic)

    # Prompt templates
    def list_prompts(self) -> list[PromptTemplateResponse]:
        return [PromptTemplateResponse.model_validate(p) for p in self.prompt_repo.get_all(limit=100)]

    def create_prompt(self, data: PromptTemplateCreate) -> PromptTemplateResponse:
        prompt = PromptTemplate(**data.model_dump())
        return PromptTemplateResponse.model_validate(self.prompt_repo.create(prompt))

    def update_prompt(self, prompt_id: int, data: PromptTemplateUpdate) -> PromptTemplateResponse:
        prompt = self.prompt_repo.get_by_id(prompt_id)
        if not prompt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(prompt, key, value)
        return PromptTemplateResponse.model_validate(self.prompt_repo.update(prompt))

    def delete_prompt(self, prompt_id: int) -> None:
        prompt = self.prompt_repo.get_by_id(prompt_id)
        if not prompt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        self.prompt_repo.delete(prompt)

    def clear_skill_cache(self, skill_id: int) -> None:
        content = self.content_repo.get_by_skill_id(skill_id)
        if content:
            self.content_repo.delete(content)
        self.quiz_repo.delete_by_skill_id(skill_id)

    # Users & analytics
    def list_users(self) -> list[UserProgressSummary]:
        from app.repositories.progress_repository import ProgressRepository

        progress_repo = ProgressRepository(self.db)
        users = self.user_repo.get_all(limit=1000)
        summaries = []
        for user in users:
            skill_progress = progress_repo.get_user_skill_progress(user.id)
            completed = sum(1 for sp in skill_progress if sp.completed)
            total = len(skill_progress) if skill_progress else 0
            overall = round((completed / total * 100) if total else 0, 1)
            summaries.append(
                UserProgressSummary(
                    id=user.id,
                    email=user.email,
                    selected_expertise=user.selected_expertise,
                    selected_roadmap=user.selected_roadmap,
                    completed_skills=completed,
                    overall_completion=overall,
                )
            )
        return summaries

    def get_analytics(self) -> AnalyticsResponse:
        from datetime import datetime, timedelta, timezone

        from app.models import QuizAttempt

        total_users = self.db.query(User).count()
        total_expertise = self.db.query(Expertise).count()
        total_roadmaps = self.db.query(Roadmap).count()
        total_skills = self.db.query(Skill).count()
        total_quiz_attempts = self.db.query(QuizAttempt).count()

        avg_score = 0.0
        attempts = self.db.query(QuizAttempt).all()
        if attempts:
            avg_score = round(sum(a.score for a in attempts) / len(attempts), 1)

        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        from app.models import UserTopicProgress

        active = (
            self.db.query(UserTopicProgress.user_id)
            .filter(UserTopicProgress.completed_at >= week_ago)
            .distinct()
            .count()
        )

        return AnalyticsResponse(
            total_users=total_users,
            total_expertise=total_expertise,
            total_roadmaps=total_roadmaps,
            total_skills=total_skills,
            total_quiz_attempts=total_quiz_attempts,
            average_quiz_score=avg_score,
            active_users_last_7_days=active,
        )

    def create_admin(self, email: str, password: str):
        from app.models import Admin

        if self.admin_repo.get_by_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin already exists")
        admin = Admin(email=email, hashed_password=get_password_hash(password))
        return self.admin_repo.create(admin)
