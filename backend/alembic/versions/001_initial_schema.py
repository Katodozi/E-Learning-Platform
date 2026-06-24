"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admins_email"), "admins", ["email"], unique=True)
    op.create_index(op.f("ix_admins_id"), "admins", ["id"], unique=False)

    op.create_table(
        "expertise",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("icon", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_expertise_id"), "expertise", ["id"], unique=False)
    op.create_index(op.f("ix_expertise_name"), "expertise", ["name"], unique=True)
    op.create_index(op.f("ix_expertise_slug"), "expertise", ["slug"], unique=True)

    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("prompt_type", sa.String(length=50), nullable=False),
        sa.Column("template", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_prompt_templates_id"), "prompt_templates", ["id"], unique=False)
    op.create_index(op.f("ix_prompt_templates_name"), "prompt_templates", ["name"], unique=True)
    op.create_index(op.f("ix_prompt_templates_prompt_type"), "prompt_templates", ["prompt_type"], unique=False)

    op.create_table(
        "roadmaps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("expertise_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("level", sa.Enum("beginner", "intermediate", "advanced", name="roadmaplevel"), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("estimated_duration", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["expertise_id"], ["expertise.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("expertise_id", "level", name="uq_roadmap_expertise_level"),
    )
    op.create_index("ix_roadmaps_expertise_id", "roadmaps", ["expertise_id"], unique=False)
    op.create_index(op.f("ix_roadmaps_id"), "roadmaps", ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("selected_expertise", sa.String(length=255), nullable=True),
        sa.Column("selected_roadmap", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["selected_roadmap"], ["roadmaps.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("roadmap_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["roadmap_id"], ["roadmaps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_skills_roadmap_id", "skills", ["roadmap_id"], unique=False)
    op.create_index(op.f("ix_skills_id"), "skills", ["id"], unique=False)

    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_topics_skill_id", "topics", ["skill_id"], unique=False)
    op.create_index(op.f("ix_topics_id"), "topics", ["id"], unique=False)

    op.create_table(
        "skill_contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("overview", sa.Text(), nullable=False),
        sa.Column("core_concepts", sa.Text(), nullable=False),
        sa.Column("basic_explanation", sa.Text(), nullable=False),
        sa.Column("real_world_example", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("skill_id"),
    )
    op.create_index("ix_skill_contents_skill_id", "skill_contents", ["skill_id"], unique=False)
    op.create_index(op.f("ix_skill_contents_id"), "skill_contents", ["id"], unique=False)

    op.create_table(
        "skill_quizzes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("questions_json", sa.Text(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("skill_id"),
    )
    op.create_index("ix_skill_quizzes_skill_id", "skill_quizzes", ["skill_id"], unique=False)
    op.create_index(op.f("ix_skill_quizzes_id"), "skill_quizzes", ["id"], unique=False)

    op.create_table(
        "user_skill_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("quiz_attempted", sa.Boolean(), nullable=False),
        sa.Column("quiz_score", sa.Float(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "skill_id", name="uq_user_skill_progress"),
    )
    op.create_index("ix_user_skill_progress_skill_id", "user_skill_progress", ["skill_id"], unique=False)
    op.create_index("ix_user_skill_progress_user_id", "user_skill_progress", ["user_id"], unique=False)
    op.create_index(op.f("ix_user_skill_progress_id"), "user_skill_progress", ["id"], unique=False)

    op.create_table(
        "user_topic_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "topic_id", name="uq_user_topic_progress"),
    )
    op.create_index("ix_user_topic_progress_topic_id", "user_topic_progress", ["topic_id"], unique=False)
    op.create_index("ix_user_topic_progress_user_id", "user_topic_progress", ["user_id"], unique=False)
    op.create_index(op.f("ix_user_topic_progress_id"), "user_topic_progress", ["id"], unique=False)

    op.create_table(
        "quiz_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("quiz_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("answers_json", sa.Text(), nullable=False),
        sa.Column("attempted_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["quiz_id"], ["skill_quizzes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_quiz_attempts_quiz_id", "quiz_attempts", ["quiz_id"], unique=False)
    op.create_index("ix_quiz_attempts_user_id", "quiz_attempts", ["user_id"], unique=False)
    op.create_index(op.f("ix_quiz_attempts_id"), "quiz_attempts", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("quiz_attempts")
    op.drop_table("user_topic_progress")
    op.drop_table("user_skill_progress")
    op.drop_table("skill_quizzes")
    op.drop_table("skill_contents")
    op.drop_table("topics")
    op.drop_table("skills")
    op.drop_table("users")
    op.drop_table("roadmaps")
    op.drop_table("prompt_templates")
    op.drop_table("expertise")
    op.drop_table("admins")
    op.execute("DROP TYPE IF EXISTS roadmaplevel")
