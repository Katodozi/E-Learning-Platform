from sqlalchemy.orm import Session, joinedload

from app.models import Expertise, Roadmap, Skill, Topic
from app.repositories.base import BaseRepository


class ExpertiseRepository(BaseRepository[Expertise]):
    def __init__(self, db: Session):
        super().__init__(db, Expertise)

    def get_by_slug(self, slug: str) -> Expertise | None:
        return self.db.query(Expertise).filter(Expertise.slug == slug).first()

    def get_all_ordered(self) -> list[Expertise]:
        return self.db.query(Expertise).order_by(Expertise.name).all()


class RoadmapRepository(BaseRepository[Roadmap]):
    def __init__(self, db: Session):
        super().__init__(db, Roadmap)

    def get_by_expertise(self, expertise_id: int) -> list[Roadmap]:
        return (
            self.db.query(Roadmap)
            .options(joinedload(Roadmap.skills))
            .filter(Roadmap.expertise_id == expertise_id)
            .order_by(Roadmap.level)
            .all()
        )

    def get_with_skills(self, roadmap_id: int) -> Roadmap | None:
        return (
            self.db.query(Roadmap)
            .options(
                joinedload(Roadmap.skills).joinedload(Skill.topics),
                joinedload(Roadmap.expertise),
            )
            .filter(Roadmap.id == roadmap_id)
            .first()
        )


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, db: Session):
        super().__init__(db, Skill)

    def get_with_topics(self, skill_id: int) -> Skill | None:
        return (
            self.db.query(Skill)
            .options(joinedload(Skill.topics), joinedload(Skill.roadmap))
            .filter(Skill.id == skill_id)
            .first()
        )


class TopicRepository(BaseRepository[Topic]):
    def __init__(self, db: Session):
        super().__init__(db, Topic)

    def get_by_skill(self, skill_id: int) -> list[Topic]:
        return (
            self.db.query(Topic)
            .filter(Topic.skill_id == skill_id)
            .order_by(Topic.order_index)
            .all()
        )
