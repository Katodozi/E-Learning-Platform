import json
import re
from typing import Any

import google.generativeai as genai
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import SkillContent, SkillQuiz
from app.repositories.progress_repository import PromptTemplateRepository, SkillContentRepository, SkillQuizRepository
from app.repositories.roadmap_repository import SkillRepository
from app.schemas.quiz import QuizQuestion

settings = get_settings()


DEFAULT_SKILL_PROMPT = """You are an expert technical educator. Generate beginner-friendly foundational content for the skill: {skill_name}.

Context: This skill is part of a {roadmap_level} roadmap in {expertise_name}.
Topics covered: {topics}

Requirements:
- Simple explanations suitable for beginners
- Technical accuracy
- No advanced tutorials
- Practical and clear

Respond ONLY with valid JSON in this exact format:
{{
  "overview": "2-3 sentence overview",
  "core_concepts": "Bullet points of core concepts as a single string with newlines",
  "basic_explanation": "Clear foundational explanation in 2-3 paragraphs",
  "real_world_example": "A practical real-world example",
  "summary": "Brief summary of key takeaways"
}}"""

DEFAULT_QUIZ_PROMPT = """You are an expert technical educator. Generate exactly 5 multiple-choice questions for the skill: {skill_name}.

Topics: {topics}
Level: Beginner-friendly foundational knowledge only.

Respond ONLY with valid JSON in this exact format:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Why this answer is correct"
    }}
  ]
}}

Rules:
- Exactly 5 questions
- Each question has exactly 4 options
- correct_answer is index 0-3
- Beginner-friendly content only"""


class GeminiService:
    def __init__(self, db: Session):
        self.db = db
        self.prompt_repo = PromptTemplateRepository(db)
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash") if settings.GEMINI_API_KEY else None

    def _extract_json(self, text: str) -> dict[str, Any]:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Invalid AI response format: {exc}",
            ) from exc

    def _get_prompt(self, prompt_type: str, default: str) -> str:
        template = self.prompt_repo.get_active_by_type(prompt_type)
        return template.template if template else default

    def _call_gemini(self, prompt: str) -> dict[str, Any]:
        if not self.model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Gemini API key not configured",
            )
        try:
            response = self.model.generate_content(prompt)
            return self._extract_json(response.text)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI generation failed: {exc}",
            ) from exc

    def _validate_skill_content(self, data: dict[str, Any]) -> dict[str, str]:
        required = ["overview", "core_concepts", "basic_explanation", "real_world_example", "summary"]
        for field in required:
            if field not in data or not isinstance(data[field], str) or not data[field].strip():
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"AI response missing valid field: {field}",
                )
        return {k: data[k].strip() for k in required}

    def _validate_quiz(self, data: dict[str, Any]) -> list[QuizQuestion]:
        questions = data.get("questions", [])
        if len(questions) != 5:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Quiz must have exactly 5 questions")
        validated = []
        for q in questions:
            question = QuizQuestion(**q)
            validated.append(question)
        return validated

    def generate_skill_content(
        self,
        skill_name: str,
        expertise_name: str,
        roadmap_level: str,
        topics: list[str],
    ) -> dict[str, str]:
        prompt_template = self._get_prompt("skill_content", DEFAULT_SKILL_PROMPT)
        prompt = prompt_template.format(
            skill_name=skill_name,
            expertise_name=expertise_name,
            roadmap_level=roadmap_level,
            topics=", ".join(topics),
        )
        data = self._call_gemini(prompt)
        return self._validate_skill_content(data)

    def generate_quiz(self, skill_name: str, topics: list[str]) -> list[QuizQuestion]:
        prompt_template = self._get_prompt("quiz", DEFAULT_QUIZ_PROMPT)
        prompt = prompt_template.format(skill_name=skill_name, topics=", ".join(topics))
        data = self._call_gemini(prompt)
        return self._validate_quiz(data)

    def get_fallback_skill_content(self, skill_name: str, topics: list[str]) -> dict[str, str]:
        topic_list = ", ".join(topics)
        return {
            "overview": f"{skill_name} is a foundational skill that helps you build practical knowledge step by step.",
            "core_concepts": f"- Understanding {skill_name} basics\n- Key terminology\n- Common patterns\n- Topics: {topic_list}",
            "basic_explanation": f"This module introduces {skill_name} in a beginner-friendly way. You'll learn the core ideas behind {topic_list} and how they connect in real projects.",
            "real_world_example": f"In a typical project, developers use {skill_name} to solve everyday problems such as organizing code, handling data, and building reliable features.",
            "summary": f"You now have a foundational understanding of {skill_name}. Continue practicing each topic and complete the quiz to reinforce your learning.",
        }

    def get_fallback_quiz(self, skill_name: str) -> list[QuizQuestion]:
        return [
            QuizQuestion(
                question=f"What is the primary purpose of {skill_name}?",
                options=["Build foundational knowledge", "Skip basics", "Avoid practice", "Ignore concepts"],
                correct_answer=0,
                explanation=f"{skill_name} helps build foundational knowledge.",
            ),
            QuizQuestion(
                question=f"Which approach best supports learning {skill_name}?",
                options=["Practice regularly", "Memorize only", "Avoid examples", "Skip topics"],
                correct_answer=0,
                explanation="Regular practice reinforces understanding.",
            ),
            QuizQuestion(
                question="What should beginners focus on first?",
                options=["Core concepts", "Advanced edge cases", "Complex optimizations", "Skipping fundamentals"],
                correct_answer=0,
                explanation="Beginners should master core concepts first.",
            ),
            QuizQuestion(
                question="Why are real-world examples useful?",
                options=["They connect theory to practice", "They replace all study", "They avoid learning", "They skip quizzes"],
                correct_answer=0,
                explanation="Examples bridge theory and practical application.",
            ),
            QuizQuestion(
                question="How do you measure skill progress?",
                options=["Complete topics and quizzes", "Ignore checkpoints", "Skip assessments", "Avoid review"],
                correct_answer=0,
                explanation="Topics and quizzes track meaningful progress.",
            ),
        ]
