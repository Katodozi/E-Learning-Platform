from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import QuizAttempt, User
from app.repositories.progress_repository import ProgressRepository
from app.repositories.roadmap_repository import RoadmapRepository
from app.schemas.dashboard import DashboardResponse


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.roadmap_repo = RoadmapRepository(db)
        self.progress_repo = ProgressRepository(db)

    def get_dashboard(self, user: User) -> DashboardResponse:
        roadmap_data = None
        total_skills = 0
        completed_skills = 0
        skill_progress_list = []

        if user.selected_roadmap:
            roadmap = self.roadmap_repo.get_with_skills(user.selected_roadmap)
            if roadmap:
                total_skills = len(roadmap.skills)
                roadmap_data = {
                    "id": roadmap.id,
                    "title": roadmap.title,
                    "level": roadmap.level.value,
                    "expertise_name": roadmap.expertise.name,
                    "estimated_duration": roadmap.estimated_duration,
                }

                for skill in roadmap.skills:
                    progress = self.progress_repo.get_skill_progress(user.id, skill.id)
                    topics_total = len(skill.topics)
                    topics_done = sum(
                        1
                        for t in skill.topics
                        if (p := self.progress_repo.get_topic_progress(user.id, t.id)) and p.completed
                    )
                    topic_pct = (topics_done / topics_total * 100) if topics_total else 0
                    is_completed = bool(progress and progress.completed)
                    if is_completed:
                        completed_skills += 1

                    skill_progress_list.append(
                        {
                            "skill_id": skill.id,
                            "skill_name": skill.name,
                            "topics_completed": topics_done,
                            "topics_total": topics_total,
                            "topic_progress": round(topic_pct, 1),
                            "quiz_score": progress.quiz_score if progress else None,
                            "completed": is_completed,
                        }
                    )

        overall = round((completed_skills / total_skills * 100) if total_skills else 0, 1)

        quiz_scores = []
        attempts = (
            self.db.query(QuizAttempt)
            .filter(QuizAttempt.user_id == user.id)
            .order_by(QuizAttempt.attempted_at.desc())
            .limit(10)
            .all()
        )
        for attempt in attempts:
            quiz_scores.append(
                {
                    "quiz_id": attempt.quiz_id,
                    "score": attempt.score,
                    "attempted_at": attempt.attempted_at.isoformat(),
                }
            )

        recent_topics = []
        topic_progress = self.progress_repo.get_user_topic_progress(user.id)[:5]
        for tp in topic_progress:
            recent_topics.append(
                {
                    "topic_id": tp.topic_id,
                    "topic_name": tp.topic.name if tp.topic else "Unknown",
                    "completed_at": tp.completed_at.isoformat() if tp.completed_at else None,
                }
            )

        streak = self._calculate_streak(user.id)
        progress_chart = self._build_progress_chart(user.id)

        return DashboardResponse(
            selected_roadmap=roadmap_data,
            overall_completion=overall,
            completed_skills=completed_skills,
            remaining_skills=max(total_skills - completed_skills, 0),
            total_skills=total_skills,
            quiz_scores=quiz_scores,
            current_streak=streak,
            recently_completed_topics=recent_topics,
            progress_chart=progress_chart,
            skill_progress=skill_progress_list,
        )

    def _calculate_streak(self, user_id: int) -> int:
        from app.models import UserTopicProgress

        records = (
            self.db.query(UserTopicProgress)
            .filter(UserTopicProgress.user_id == user_id, UserTopicProgress.completed.is_(True))
            .order_by(UserTopicProgress.completed_at.desc())
            .all()
        )
        if not records:
            return 0

        streak = 0
        current_date = datetime.now(timezone.utc).date()
        completed_dates = set()
        for r in records:
            if r.completed_at:
                completed_dates.add(r.completed_at.date())

        while current_date in completed_dates or (streak == 0 and (current_date - timedelta(days=1)) in completed_dates):
            if current_date in completed_dates:
                streak += 1
            current_date -= timedelta(days=1)
            if streak > 0 and current_date not in completed_dates:
                break

        return streak

    def _build_progress_chart(self, user_id: int) -> list[dict]:
        from app.models import UserTopicProgress

        chart = []
        today = datetime.now(timezone.utc).date()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            count = (
                self.db.query(UserTopicProgress)
                .filter(
                    UserTopicProgress.user_id == user_id,
                    UserTopicProgress.completed.is_(True),
                )
                .all()
            )
            day_count = sum(1 for c in count if c.completed_at and c.completed_at.date() == day)
            chart.append({"date": day.isoformat(), "topics_completed": day_count})
        return chart
