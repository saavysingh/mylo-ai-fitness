# mylo_ai_fitness/models/prompt.py
from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class PromptContext(BaseModel):
    user_basics: Dict[str, Any]
    goals_summary: str
    experience_level: str
    constraints: List[str]
    preferences: List[str]
    workout_focus: str
    estimated_duration: str


class PromptTemplate(BaseModel):
    name: str
    system_prompt: str
    user_prompt_template: str
    expected_format: str
    example_output: Optional[str] = None

