from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.repositories.progress_repository import ProgressRepository
from app.repositories.roadmap_repository import ExpertiseRepository, RoadmapRepository, SkillRepository
from app.schemas.roadmap import (
    ExpertiseResponse,
    RoadmapDetail,
    RoadmapSummary,
    SkillSummary,
    TopicResponse,
)


class RoadmapService:
    def __init__(self, db: Session):
        self.expertise_repo = ExpertiseRepository(db)
        self.roadmap_repo = RoadmapRepository(db)
        self.skill_repo = SkillRepository(db)
        self.progress_repo = ProgressRepository(db)

    def list_expertise(self) -> list[ExpertiseResponse]:
        expertise_list = self.expertise_repo.get_all_ordered()
        return [ExpertiseResponse.model_validate(e) for e in expertise_list]

    def get_roadmaps_by_expertise(self, expertise_id: int) -> list[RoadmapSummary]:
        expertise = self.expertise_repo.get_by_id(expertise_id)
        if not expertise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expertise not found")
        roadmaps = self.roadmap_repo.get_by_expertise(expertise_id)
        return [
            RoadmapSummary(
                id=r.id,
                title=r.title,
                level=r.level.value,
                description=r.description,
                estimated_duration=r.estimated_duration,
                skill_count=len(r.skills),
            )
            for r in roadmaps
        ]

    def get_roadmap_detail(self, roadmap_id: int, user: User | None = None) -> RoadmapDetail:
        roadmap = self.roadmap_repo.get_with_skills(roadmap_id)
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")

        skills = []
        for skill in roadmap.skills:
            topics_completed = 0
            if user:
                for topic in skill.topics:
                    progress = self.progress_repo.get_topic_progress(user.id, topic.id)
                    if progress and progress.completed:
                        topics_completed += 1

            skills.append(
                SkillSummary(
                    id=skill.id,
                    name=skill.name,
                    description=skill.description,
                    order_index=skill.order_index,
                    topic_count=len(skill.topics),
                )
            )

        return RoadmapDetail(
            id=roadmap.id,
            title=roadmap.title,
            level=roadmap.level.value,
            description=roadmap.description,
            estimated_duration=roadmap.estimated_duration,
            expertise_id=roadmap.expertise_id,
            expertise_name=roadmap.expertise.name,
            skills=skills,
        )

    def get_skill_with_topics(self, skill_id: int, user: User | None = None):
        skill = self.skill_repo.get_with_topics(skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

        topics = []
        for topic in skill.topics:
            completed = False
            if user:
                progress = self.progress_repo.get_topic_progress(user.id, topic.id)
                completed = bool(progress and progress.completed)
            topics.append(
                TopicResponse(
                    id=topic.id,
                    name=topic.name,
                    description=topic.description,
                    order_index=topic.order_index,
                    completed=completed,
                )
            )
        return skill, topics
