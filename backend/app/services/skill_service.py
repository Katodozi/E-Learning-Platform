from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import SkillContent, User
from app.repositories.progress_repository import ProgressRepository, SkillContentRepository
from app.repositories.roadmap_repository import SkillRepository
from app.schemas.skill import SkillContentResponse, TopicCompleteRequest, TopicCompleteResponse
from app.services.gemini.gemini_service import GeminiService

settings = get_settings()


class SkillService:
    def __init__(self, db: Session):
        self.db = db
        self.skill_repo = SkillRepository(db)
        self.content_repo = SkillContentRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.gemini = GeminiService(db)

    def get_skill_content(self, skill_id: int, user: User) -> SkillContentResponse:
        skill = self.skill_repo.get_with_topics(skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

        cached = self.content_repo.get_by_skill_id(skill_id)
        if cached:
            content = cached
            is_cached = True
        else:
            topics = [t.name for t in skill.topics]
            try:
                if settings.GEMINI_API_KEY:
                    generated = self.gemini.generate_skill_content(
                        skill_name=skill.name,
                        expertise_name=skill.roadmap.expertise.name,
                        roadmap_level=skill.roadmap.level.value,
                        topics=topics,
                    )
                else:
                    generated = self.gemini.get_fallback_skill_content(skill.name, topics)
            except HTTPException:
                generated = self.gemini.get_fallback_skill_content(skill.name, topics)

            content = SkillContent(
                skill_id=skill_id,
                overview=generated["overview"],
                core_concepts=generated["core_concepts"],
                basic_explanation=generated["basic_explanation"],
                real_world_example=generated["real_world_example"],
                summary=generated["summary"],
            )
            content = self.content_repo.create(content)
            is_cached = False

        topic_list = []
        for topic in skill.topics:
            progress = self.progress_repo.get_topic_progress(user.id, topic.id)
            topic_list.append(
                {
                    "id": topic.id,
                    "name": topic.name,
                    "description": topic.description,
                    "completed": bool(progress and progress.completed),
                }
            )

        return SkillContentResponse(
            skill_id=skill.id,
            skill_name=skill.name,
            overview=content.overview,
            core_concepts=content.core_concepts,
            basic_explanation=content.basic_explanation,
            real_world_example=content.real_world_example,
            summary=content.summary,
            topics=topic_list,
            cached=is_cached,
        )

    def complete_topic(self, user: User, data: TopicCompleteRequest) -> TopicCompleteResponse:
        from app.repositories.roadmap_repository import TopicRepository

        topic_repo = TopicRepository(self.db)
        topic = topic_repo.get_by_id(data.topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

        progress = self.progress_repo.mark_topic_complete(user.id, data.topic_id)
        skill = self.skill_repo.get_with_topics(topic.skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

        all_topics_done = all(
            (p := self.progress_repo.get_topic_progress(user.id, t.id)) and p.completed for t in skill.topics
        )
        skill_progress = self.progress_repo.get_or_create_skill_progress(user.id, skill.id)
        quiz_attempted = skill_progress.quiz_attempted
        skill_completed = all_topics_done and quiz_attempted

        self.progress_repo.update_skill_progress(
            user.id,
            skill.id,
            completed=skill_completed,
            quiz_attempted=quiz_attempted,
            quiz_score=skill_progress.quiz_score,
        )

        return TopicCompleteResponse(
            topic_id=data.topic_id,
            completed=progress.completed,
            completed_at=progress.completed_at.isoformat() if progress.completed_at else None,
            skill_progress={
                "skill_id": skill.id,
                "all_topics_completed": all_topics_done,
                "quiz_attempted": quiz_attempted,
                "skill_completed": skill_completed,
            },
        )
