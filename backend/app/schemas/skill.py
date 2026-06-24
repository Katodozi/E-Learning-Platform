from pydantic import BaseModel, ConfigDict, Field


class SkillContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_id: int
    skill_name: str
    overview: str
    core_concepts: str
    basic_explanation: str
    real_world_example: str
    summary: str
    topics: list[dict] = []
    cached: bool = False


class TopicCompleteRequest(BaseModel):
    topic_id: int


class TopicCompleteResponse(BaseModel):
    topic_id: int
    completed: bool
    completed_at: str | None
    skill_progress: dict
