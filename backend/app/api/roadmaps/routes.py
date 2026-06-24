from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_optional_user
from app.database.session import get_db
from app.models import User
from app.schemas.roadmap import ExpertiseResponse, RoadmapDetail, RoadmapSummary
from app.services.roadmap_service import RoadmapService

router = APIRouter(tags=["roadmaps"])


@router.get("/expertise", response_model=list[ExpertiseResponse])
def list_expertise(db: Session = Depends(get_db)):
    return RoadmapService(db).list_expertise()


@router.get("/roadmaps/{expertise_id}", response_model=list[RoadmapSummary])
def get_roadmaps_by_expertise(expertise_id: int, db: Session = Depends(get_db)):
    return RoadmapService(db).get_roadmaps_by_expertise(expertise_id)


@router.get("/roadmap/{roadmap_id}", response_model=RoadmapDetail)
def get_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    return RoadmapService(db).get_roadmap_detail(roadmap_id, current_user)
