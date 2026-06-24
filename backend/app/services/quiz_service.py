import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import SkillQuiz, User
from app.repositories.progress_repository import ProgressRepository, QuizAttemptRepository, SkillQuizRepository
from app.repositories.roadmap_repository import SkillRepository
from app.schemas.quiz import QuizGenerateRequest, QuizGenerateResponse, QuizQuestion, QuizSubmitRequest, QuizSubmitResponse
from app.services.gemini.gemini_service import GeminiService

settings = get_settings()


def proficiency_label(score: float) -> str:
    if score >= 90:
        return "Expert"
    if score >= 70:
        return "Proficient"
    if score >= 50:
        return "Developing"
    return "Beginner"


class QuizService:
    def __init__(self, db: Session):
        self.db = db
        self.skill_repo = SkillRepository(db)
        self.quiz_repo = SkillQuizRepository(db)
        self.attempt_repo = QuizAttemptRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.gemini = GeminiService(db)

    def _all_topics_completed(self, user: User, skill_id: int) -> bool:
        skill = self.skill_repo.get_with_topics(skill_id)
        if not skill:
            return False
        for topic in skill.topics:
            progress = self.progress_repo.get_topic_progress(user.id, topic.id)
            if not progress or not progress.completed:
                return False
        return True

    def generate_quiz(self, user: User, data: QuizGenerateRequest) -> QuizGenerateResponse:
        skill = self.skill_repo.get_with_topics(data.skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

        if not self._all_topics_completed(user, data.skill_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complete all topics before taking the quiz",
            )

        cached_quiz = self.quiz_repo.get_by_skill_id(data.skill_id)
        if cached_quiz:
            questions = [QuizQuestion(**q) for q in json.loads(cached_quiz.questions_json)]
            return QuizGenerateResponse(skill_id=data.skill_id, questions=questions, cached=True)

        topics = [t.name for t in skill.topics]
        try:
            if settings.GEMINI_API_KEY:
                questions = self.gemini.generate_quiz(skill.name, topics)
            else:
                questions = self.gemini.get_fallback_quiz(skill.name)
        except HTTPException:
            questions = self.gemini.get_fallback_quiz(skill.name)

        quiz = SkillQuiz(
            skill_id=data.skill_id,
            questions_json=json.dumps([q.model_dump() for q in questions]),
        )
        self.quiz_repo.create(quiz)
        return QuizGenerateResponse(skill_id=data.skill_id, questions=questions, cached=False)

    def submit_quiz(self, user: User, data: QuizSubmitRequest) -> QuizSubmitResponse:
        skill = self.skill_repo.get_with_topics(data.skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

        quiz = self.quiz_repo.get_by_skill_id(data.skill_id)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz not generated yet")

        questions = json.loads(quiz.questions_json)
        if len(data.answers) != len(questions):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid number of answers")

        correct_count = 0
        results = []
        for i, question in enumerate(questions):
            is_correct = data.answers[i] == question["correct_answer"]
            if is_correct:
                correct_count += 1
            results.append(
                {
                    "question": question["question"],
                    "your_answer": data.answers[i],
                    "correct_answer": question["correct_answer"],
                    "is_correct": is_correct,
                    "explanation": question["explanation"],
                }
            )

        score = round((correct_count / len(questions)) * 100, 2)

        from app.models import QuizAttempt

        attempt = QuizAttempt(
            user_id=user.id,
            quiz_id=quiz.id,
            score=score,
            answers_json=json.dumps(data.answers),
        )
        self.attempt_repo.create(attempt)

        all_topics_done = self._all_topics_completed(user, data.skill_id)
        skill_completed = all_topics_done and True
        self.progress_repo.update_skill_progress(
            user.id,
            data.skill_id,
            completed=skill_completed,
            quiz_attempted=True,
            quiz_score=score,
        )

        return QuizSubmitResponse(
            skill_id=data.skill_id,
            score=score,
            proficiency=proficiency_label(score),
            correct_count=correct_count,
            total_questions=len(questions),
            results=results,
        )
