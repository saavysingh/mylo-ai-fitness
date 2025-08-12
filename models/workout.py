from typing import List, Optional
from pydantic import BaseModel, Field

class Exercise(BaseModel):
    name: str
    duration: str
    instructions: str
    modifications: str

class WorkoutSection(BaseModel):
    name: str
    duration: str
    exercises: List[Exercise]

class WorkoutPlan(BaseModel):
    title: str
    description: str
    total_duration: str
    difficulty: str
    sections: List[WorkoutSection]
    notes: List[str]
    progression: str