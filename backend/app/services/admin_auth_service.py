from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories.admin_repository import AdminRepository
from app.schemas.auth import AdminLogin, AdminResponse


class AdminAuthService:
    def __init__(self, db: Session):
        self.db = db
        self.admin_repo = AdminRepository(db)

    def login(self, data: AdminLogin) -> tuple[AdminResponse, str]:
        admin = self.admin_repo.get_by_email(data.email)
        if not admin or not verify_password(data.password, admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
        token = create_access_token({"sub": str(admin.id), "type": "admin"})
        return AdminResponse.model_validate(admin), token
