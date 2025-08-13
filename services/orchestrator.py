from typing import Dict
import logging
import requests
import json

from models.user import UserProfile
from core.config import GROQ_API_KEY
from models.schemas import Basics, GoalBlock, PrefsConstraints

class WorkoutOrchestrator:
    """
    Simple orchestrator for 3-step workflow:
    1. Basic info - concise response
    2. Goals - concise response  
    3. Generate workout - detailed response
    """
    
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.logger = logging.getLogger(__name__)

    def _call_llm(self, system_prompt: str, user_prompt: str, max_tokens: int = 150) -> str:
        """Simple LLM call helper"""
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                self.logger.error(f"LLM API error: {response.status_code}")
                return "I apologize, but I'm having trouble processing your request right now."
                
        except Exception as e:
            self.logger.error(f"LLM call failed: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now."

    def analyze_basic_info(self, basics: Basics) -> Dict:
        """First LLM call - concise response to basic info"""
        try:
            system_prompt = "You are Mylo, a friendly AI fitness coach. Respond briefly and warmly to acknowledge the user's basic information."
            
            user_prompt = f"""User Info: Age {basics.age}, {basics.gender}, {basics.height_cm}cm, {basics.weight_kg}kg, {basics.activity_level} activity level.

Provide a brief (2-3 sentences), warm acknowledgment and show enthusiasm for helping them."""

            response = self._call_llm(system_prompt, user_prompt, max_tokens=100)
            
            return {
                "status": "success",
                "message": response
            }
            
        except Exception as e:
            self.logger.error(f"Basic info analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": "Thanks! I've recorded your basic information."
            }

    def analyze_goals(self, basics: Basics, goals: GoalBlock) -> Dict:
        """Second LLM call - concise response to goals"""
        try:
            system_prompt = "You are Mylo, a friendly AI fitness coach. Respond briefly and encouragingly to acknowledge the user's fitness goals."
            
            user_prompt = f"""User Profile: {basics.age}yr old {basics.gender}, {basics.activity_level} activity level.
Goals: {', '.join(goals.goals)}

Provide a brief (2-3 sentences), encouraging response about their goals."""

            response = self._call_llm(system_prompt, user_prompt, max_tokens=100)
            
            return {
                "status": "success",
                "message": response
            }
            
        except Exception as e:
            self.logger.error(f"Goals analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": "Great! I've recorded your fitness goals."
            }

    def generate_workout(self, user_profile: UserProfile) -> Dict:
        """Third LLM call - generate detailed workout plan"""
        try:
            system_prompt = """You are Mylo, an expert AI fitness coach. Create a comprehensive, personalized workout plan based on the user's profile. 

Format your response as a clear, structured workout plan with:
- Workout title and description
- Warm-up section (5-10 minutes)
- Main workout section (20-45 minutes)
- Cool-down section (5-10 minutes)
- Each exercise should include: name, reps/duration, brief instructions

Make it engaging and motivating."""
            
            # Build user context
            goals_text = ", ".join([goal.goal_type for goal in user_profile.goals])
            equipment_text = ", ".join(user_profile.restrictions.equipment) if user_profile.restrictions.equipment else "bodyweight only"
            workout_types_text = ", ".join(user_profile.preferences.preferred_workout_types) if user_profile.preferences.preferred_workout_types else "any type"
            
            user_prompt = f"""Create a personalized workout for:

USER PROFILE:
- Age: {user_profile.physical_stats.age}
- Gender: {user_profile.physical_stats.gender}
- Activity Level: {user_profile.activity_level}
- Goals: {goals_text}
- Available Equipment: {equipment_text}
- Preferred Workout Types: {workout_types_text}
- Injuries/Restrictions: {', '.join(user_profile.restrictions.injuries) if user_profile.restrictions.injuries else 'none'}

Please create a complete workout plan that's safe, effective, and aligned with their goals."""

            response = self._call_llm(system_prompt, user_prompt, max_tokens=2000)
            
            return {
                "status": "success",
                "workout": response
            }
            
        except Exception as e:
            self.logger.error(f"Workout generation failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }


