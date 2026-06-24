from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, data: UserRegister) -> tuple[UserResponse, str]:
        if self.user_repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user = User(
            email=data.email,
            hashed_password=get_password_hash(data.password),
            selected_expertise=data.selected_expertise,
            selected_roadmap=data.selected_roadmap,
        )
        user = self.user_repo.create(user)
        token = create_access_token({"sub": str(user.id), "type": "user"})
        return UserResponse.model_validate(user), token

    def login(self, data: UserLogin) -> tuple[UserResponse, str]:
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token({"sub": str(user.id), "type": "user"})
        return UserResponse.model_validate(user), token

    def get_me(self, user: User) -> UserResponse:
        return UserResponse.model_validate(user)
