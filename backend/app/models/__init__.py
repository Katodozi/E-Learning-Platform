import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RoadmapLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    selected_expertise: Mapped[str | None] = mapped_column(String(255), nullable=True)
    selected_roadmap: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("roadmaps.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    roadmap: Mapped["Roadmap | None"] = relationship("Roadmap", back_populates="users")
    topic_progress: Mapped[list["UserTopicProgress"]] = relationship(
        "UserTopicProgress", back_populates="user", cascade="all, delete-orphan"
    )
    skill_progress: Mapped[list["UserSkillProgress"]] = relationship(
        "UserSkillProgress", back_populates="user", cascade="all, delete-orphan"
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="user", cascade="all, delete-orphan"
    )


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class Expertise(Base):
    __tablename__ = "expertise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(100), nullable=False, default="code")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    roadmaps: Mapped[list["Roadmap"]] = relationship(
        "Roadmap", back_populates="expertise", cascade="all, delete-orphan"
    )


class Roadmap(Base):
    __tablename__ = "roadmaps"
    __table_args__ = (
        UniqueConstraint("expertise_id", "level", name="uq_roadmap_expertise_level"),
        Index("ix_roadmaps_expertise_id", "expertise_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    expertise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("expertise.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[RoadmapLevel] = mapped_column(
        Enum(RoadmapLevel, name="roadmaplevel", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_duration: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    expertise: Mapped["Expertise"] = relationship("Expertise", back_populates="roadmaps")
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", back_populates="roadmap", cascade="all, delete-orphan", order_by="Skill.order_index"
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="roadmap")


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (Index("ix_skills_roadmap_id", "roadmap_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    roadmap_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="skills")
    topics: Mapped[list["Topic"]] = relationship(
        "Topic", back_populates="skill", cascade="all, delete-orphan", order_by="Topic.order_index"
    )
    content: Mapped["SkillContent | None"] = relationship(
        "SkillContent", back_populates="skill", uselist=False, cascade="all, delete-orphan"
    )
    quiz: Mapped["SkillQuiz | None"] = relationship(
        "SkillQuiz", back_populates="skill", uselist=False, cascade="all, delete-orphan"
    )
    user_progress: Mapped[list["UserSkillProgress"]] = relationship(
        "UserSkillProgress", back_populates="skill", cascade="all, delete-orphan"
    )


class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (Index("ix_topics_skill_id", "skill_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="topics")
    user_progress: Mapped[list["UserTopicProgress"]] = relationship(
        "UserTopicProgress", back_populates="topic", cascade="all, delete-orphan"
    )


class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_user_topic_progress"),
        Index("ix_user_topic_progress_user_id", "user_id"),
        Index("ix_user_topic_progress_topic_id", "topic_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="topic_progress")
    topic: Mapped["Topic"] = relationship("Topic", back_populates="user_progress")


class UserSkillProgress(Base):
    __tablename__ = "user_skill_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill_progress"),
        Index("ix_user_skill_progress_user_id", "user_id"),
        Index("ix_user_skill_progress_skill_id", "skill_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    quiz_attempted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    quiz_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="skill_progress")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="user_progress")


class SkillContent(Base):
    __tablename__ = "skill_contents"
    __table_args__ = (Index("ix_skill_contents_skill_id", "skill_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    core_concepts: Mapped[str] = mapped_column(Text, nullable=False)
    basic_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    real_world_example: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="content")


class SkillQuiz(Base):
    __tablename__ = "skill_quizzes"
    __table_args__ = (Index("ix_skill_quizzes_skill_id", "skill_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    questions_json: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="quiz")
    attempts: Mapped[list["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="quiz", cascade="all, delete-orphan"
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    __table_args__ = (
        Index("ix_quiz_attempts_user_id", "user_id"),
        Index("ix_quiz_attempts_quiz_id", "quiz_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skill_quizzes.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    answers_json: Mapped[str] = mapped_column(Text, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="quiz_attempts")
    quiz: Mapped["SkillQuiz"] = relationship("SkillQuiz", back_populates="attempts")


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    prompt_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    template: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )
