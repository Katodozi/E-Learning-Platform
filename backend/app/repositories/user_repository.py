from sqlalchemy.orm import Session, joinedload

from app.models import Roadmap, User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_with_roadmap(self, user_id: int) -> User | None:
        return (
            self.db.query(User)
            .options(joinedload(User.roadmap).joinedload(Roadmap.expertise))
            .filter(User.id == user_id)
            .first()
        )
