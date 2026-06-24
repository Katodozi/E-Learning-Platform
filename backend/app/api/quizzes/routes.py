from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models import User
from app.schemas.quiz import QuizGenerateRequest, QuizGenerateResponse, QuizSubmitRequest, QuizSubmitResponse
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizGenerateResponse)
def generate_quiz(
    data: QuizGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return QuizService(db).generate_quiz(current_user, data)


@router.post("/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    data: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return QuizService(db).submit_quiz(current_user, data)
