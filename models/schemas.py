from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# Enums and Allowlists
GENDER = ["male", "female", "other", "prefer_not_to_say"]
ACTIVITY = ["sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"]
GOALS = ["weight_loss", "muscle_gain", "endurance", "strength", "flexibility", "maintenance"]
EQUIPMENT = ["bodyweight", "dumbbells", "resistance_bands", "gym_access"]
WORKOUT_TYPES = ["cardio", "strength_training", "yoga", "pilates", "HIIT"]
TIMES = ["morning", "afternoon", "evening"]

class ChatStage(str, Enum):
    BASIC = "basic"
    GOALS = "goals"
    FINAL = "final"

class Basics(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None

class GoalBlock(BaseModel):
    goals: List[str] = Field(default_factory=list)

class PrefsConstraints(BaseModel):
    injuries: List[str] = Field(default_factory=list)
    equipment: List[str] = Field(default_factory=list)
    preferred_workout_types: List[str] = Field(default_factory=list)
    preferred_training_times: List[str] = Field(default_factory=list)
# Removed unused time_per_session_min field
    not_preferred_exercises: List[str] = Field(default_factory=list)
    special_considerations: List[str] = Field(default_factory=list)

class ConversationState(BaseModel):
    session_id: str
    stage: ChatStage
    basics: Optional[Basics] = None
    goals_block: Optional[GoalBlock] = None
    prefs: Optional[PrefsConstraints] = None
    missing: List[str] = Field(default_factory=list)

# Removed unused response models - using simplified ChatOut instead

class ChatIn(BaseModel):
    session_id: str
    stage: ChatStage
    message: str = ""
    selections: Dict = Field(default_factory=dict)

class ChatOut(BaseModel):
    assistant_text: str
    state: ConversationState
    next_stage: ChatStage
    controls: Dict = Field(default_factory=dict)
    followup: Optional[str] = None
