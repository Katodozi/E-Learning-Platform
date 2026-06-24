from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: int = Field(ge=0, le=3)
    explanation: str


class QuizGenerateRequest(BaseModel):
    skill_id: int


class QuizGenerateResponse(BaseModel):
    skill_id: int
    questions: list[QuizQuestion]
    cached: bool = False


class QuizSubmitRequest(BaseModel):
    skill_id: int
    answers: list[int] = Field(min_length=5, max_length=5)


class QuizSubmitResponse(BaseModel):
    skill_id: int
    score: float
    proficiency: str
    correct_count: int
    total_questions: int
    results: list[dict]
