# mylo_ai_fitness/models/user.py
from datetime import datetime
from pydantic import BaseModel
from typing import List


class PhysicalStats(BaseModel):
    height: float  # in cm
    weight: float  # in kg
    gender: str
    age: int  # in years

class FitnessGoal(BaseModel):
    goal_type: str  # e.g., weight loss, muscle gain, endurance

class UserPreferences(BaseModel):
    preferred_workout_types: List[str]  # e.g., cardio, strength training, yoga
    preferred_training_times: List[str]  # e.g., morning, evening

class Restrictions(BaseModel):
    injuries: List[str]   # e.g., knee injury, back pain
    equipment: List[str]  # e.g., no equipment, limited access to gym
    not_preferred_exercises: List[str]  # e.g., burpees, pull-ups
    special_considerations: List[str]  # e.g., pregnancy, post-surgery

    @property
    def constraints(self) -> List[str]:
        """Combine all restrictions into a list of constraints"""
        constraints = []
        if self.injuries:
            constraints.extend(self.injuries)
        if self.special_considerations:
            constraints.extend(self.special_considerations)
        if self.not_preferred_exercises:
            constraints.append(f"Avoid: {', '.join(self.not_preferred_exercises)}")
        return constraints

class UserProfile(BaseModel):
    user_id: str
    name: str
    physical_stats: PhysicalStats
    goals: List[FitnessGoal]
    preferences: UserPreferences
    activity_level: str
    restrictions: Restrictions  # injuries, equipment
    created_at: datetime | None

