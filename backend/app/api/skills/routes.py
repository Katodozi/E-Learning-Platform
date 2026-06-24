from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models import User
from app.schemas.skill import SkillContentResponse, TopicCompleteRequest, TopicCompleteResponse
from app.services.skill_service import SkillService

router = APIRouter(tags=["skills"])


@router.get("/skills/{skill_id}", response_model=SkillContentResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return SkillService(db).get_skill_content(skill_id, current_user)


@router.post("/topics/complete", response_model=TopicCompleteResponse)
def complete_topic(
    data: TopicCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SkillService(db).complete_topic(current_user, data)
