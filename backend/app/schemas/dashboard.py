from pydantic import BaseModel, ConfigDict


class DashboardResponse(BaseModel):
    selected_roadmap: dict | None
    overall_completion: float
    completed_skills: int
    remaining_skills: int
    total_skills: int
    quiz_scores: list[dict]
    current_streak: int
    recently_completed_topics: list[dict]
    progress_chart: list[dict]
    skill_progress: list[dict]


class PromptTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    prompt_type: str
    template: str
    is_active: bool


class PromptTemplateCreate(BaseModel):
    name: str
    prompt_type: str
    template: str
    is_active: bool = True


class PromptTemplateUpdate(BaseModel):
    name: str | None = None
    prompt_type: str | None = None
    template: str | None = None
    is_active: bool | None = None


class UserProgressSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    selected_expertise: str | None
    selected_roadmap: int | None
    completed_skills: int
    overall_completion: float


class AnalyticsResponse(BaseModel):
    total_users: int
    total_expertise: int
    total_roadmaps: int
    total_skills: int
    total_quiz_attempts: int
    average_quiz_score: float
    active_users_last_7_days: int
