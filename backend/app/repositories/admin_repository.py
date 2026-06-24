from sqlalchemy.orm import Session

from app.models import Admin
from app.repositories.base import BaseRepository


class AdminRepository(BaseRepository[Admin]):
    def __init__(self, db: Session):
        super().__init__(db, Admin)

    def get_by_email(self, email: str) -> Admin | None:
        return self.db.query(Admin).filter(Admin.email == email).first()
