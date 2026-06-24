from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models import (
    PromptTemplate,
    QuizAttempt,
    SkillContent,
    SkillQuiz,
    UserSkillProgress,
    UserTopicProgress,
)
from app.repositories.base import BaseRepository


class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_topic_progress(self, user_id: int, topic_id: int) -> UserTopicProgress | None:
        return (
            self.db.query(UserTopicProgress)
            .filter(UserTopicProgress.user_id == user_id, UserTopicProgress.topic_id == topic_id)
            .first()
        )

    def mark_topic_complete(self, user_id: int, topic_id: int) -> UserTopicProgress:
        progress = self.get_topic_progress(user_id, topic_id)
        if progress:
            progress.completed = True
            progress.completed_at = datetime.now(timezone.utc)
        else:
            progress = UserTopicProgress(
                user_id=user_id,
                topic_id=topic_id,
                completed=True,
                completed_at=datetime.now(timezone.utc),
            )
            self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)
        return progress

    def get_skill_progress(self, user_id: int, skill_id: int) -> UserSkillProgress | None:
        return (
            self.db.query(UserSkillProgress)
            .filter(UserSkillProgress.user_id == user_id, UserSkillProgress.skill_id == skill_id)
            .first()
        )

    def get_or_create_skill_progress(self, user_id: int, skill_id: int) -> UserSkillProgress:
        progress = self.get_skill_progress(user_id, skill_id)
        if not progress:
            progress = UserSkillProgress(user_id=user_id, skill_id=skill_id)
            self.db.add(progress)
            self.db.commit()
            self.db.refresh(progress)
        return progress

    def get_user_topic_progress(self, user_id: int) -> list[UserTopicProgress]:
        return (
            self.db.query(UserTopicProgress)
            .filter(UserTopicProgress.user_id == user_id, UserTopicProgress.completed.is_(True))
            .order_by(UserTopicProgress.completed_at.desc())
            .all()
        )

    def get_user_skill_progress(self, user_id: int) -> list[UserSkillProgress]:
        return self.db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user_id).all()

    def update_skill_progress(
        self,
        user_id: int,
        skill_id: int,
        completed: bool,
        quiz_attempted: bool,
        quiz_score: float | None = None,
    ) -> UserSkillProgress:
        progress = self.get_or_create_skill_progress(user_id, skill_id)
        progress.completed = completed
        progress.quiz_attempted = quiz_attempted
        if quiz_score is not None:
            progress.quiz_score = quiz_score
        if completed:
            progress.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(progress)
        return progress


class SkillContentRepository(BaseRepository[SkillContent]):
    def __init__(self, db: Session):
        super().__init__(db, SkillContent)

    def get_by_skill_id(self, skill_id: int) -> SkillContent | None:
        return self.db.query(SkillContent).filter(SkillContent.skill_id == skill_id).first()


class SkillQuizRepository(BaseRepository[SkillQuiz]):
    def __init__(self, db: Session):
        super().__init__(db, SkillQuiz)

    def get_by_skill_id(self, skill_id: int) -> SkillQuiz | None:
        return self.db.query(SkillQuiz).filter(SkillQuiz.skill_id == skill_id).first()

    def delete_by_skill_id(self, skill_id: int) -> None:
        quiz = self.get_by_skill_id(skill_id)
        if quiz:
            self.delete(quiz)


class QuizAttemptRepository(BaseRepository[QuizAttempt]):
    def __init__(self, db: Session):
        super().__init__(db, QuizAttempt)

    def get_user_attempts(self, user_id: int) -> list[QuizAttempt]:
        return (
            self.db.query(QuizAttempt)
            .filter(QuizAttempt.user_id == user_id)
            .order_by(QuizAttempt.attempted_at.desc())
            .all()
        )

    def get_latest_attempt(self, user_id: int, quiz_id: int) -> QuizAttempt | None:
        return (
            self.db.query(QuizAttempt)
            .filter(QuizAttempt.user_id == user_id, QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.attempted_at.desc())
            .first()
        )


class PromptTemplateRepository(BaseRepository[PromptTemplate]):
    def __init__(self, db: Session):
        super().__init__(db, PromptTemplate)

    def get_active_by_type(self, prompt_type: str) -> PromptTemplate | None:
        return (
            self.db.query(PromptTemplate)
            .filter(PromptTemplate.prompt_type == prompt_type, PromptTemplate.is_active.is_(True))
            .first()
        )

    def get_by_name(self, name: str) -> PromptTemplate | None:
        return self.db.query(PromptTemplate).filter(PromptTemplate.name == name).first()
