from pydantic import BaseModel, ConfigDict, Field


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    order_index: int
    completed: bool = False


class SkillSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    order_index: int
    topic_count: int = 0


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    order_index: int
    topics: list[TopicResponse] = []


class RoadmapSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    description: str
    estimated_duration: str
    skill_count: int = 0


class RoadmapDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    description: str
    estimated_duration: str
    expertise_id: int
    expertise_name: str
    skills: list[SkillSummary] = []


class ExpertiseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str
    icon: str


class ExpertiseCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255)
    description: str
    icon: str = "code"


class ExpertiseUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    icon: str | None = None


class RoadmapCreate(BaseModel):
    expertise_id: int
    title: str
    level: str
    description: str
    estimated_duration: str


class RoadmapUpdate(BaseModel):
    title: str | None = None
    level: str | None = None
    description: str | None = None
    estimated_duration: str | None = None


class SkillCreate(BaseModel):
    roadmap_id: int
    name: str
    description: str
    order_index: int = 0


class SkillUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    order_index: int | None = None


class TopicCreate(BaseModel):
    skill_id: int
    name: str
    description: str
    order_index: int = 0


class TopicUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    order_index: int | None = None
