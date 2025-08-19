from typing import Dict
import requests

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
                return "I apologize, but I'm having trouble processing your request right now."
                
        except Exception:
            return "I apologize, but I'm having trouble processing your request right now."

    def analyze_basic_info(self, basics: Basics) -> Dict:
        """First LLM call - concise response to basic info"""
        try:
            system_prompt = """You are Mylo, a friendly, human-sounding fitness coach.
                Task: acknowledge the user's basic info in a warm, natural way (not robotic), and smoothly invite them to share their goals next.
                Tone: conversational, compact, encouraging; use contractions; no emojis; no markdown.
                Length: 1–2 sentences total.
                Avoid: restating every number; medical advice; questions about missing info (the app already has it)."""
            
            user_prompt = f"""User Info: Age {basics.age}, {basics.gender}, {basics.height_cm}cm, {basics.weight_kg}kg, {basics.activity_level} activity level.

                Write 1–2 friendly sentences that sound like a human coach.
                Briefly reflect the context (e.g., activity level or life stage) and invite them to share goals next."""

            response = self._call_llm(system_prompt, user_prompt, max_tokens=100)
            
            return {
                "status": "success",
                "message": response
            }
            
        except Exception:
            return {
                "status": "error",
                "message": "Thanks! I've recorded your basic information."
            }

    def analyze_goals(self, basics: Basics, goals: GoalBlock) -> Dict:
        """Second LLM call - concise response to goals"""
        try:
            system_prompt = """You are Mylo, a motivating, down-to-earth fitness coach.
                Task: reflect the user's goals in a natural way, give a crisp “here’s how we’ll approach it” line, and invite them to start today's session.
                Tone: conversational and concise; use contractions; no emojis; no markdown.
                Length: 2–3 sentences total.
                Avoid: interrogations or checklists. No clarifying questions are needed."""
            
            user_prompt = f"""User Profile: {basics.age}yr old {basics.gender}, {basics.height_cm}cm, {basics.weight_kg}kg, {basics.activity_level} activity level.
                Goals: {', '.join(goals.goals)}

                Write 2–3 sentences:
                - Briefly validate and reflect these goals in natural language.
                - Name 1–2 focus ideas (e.g., progressive overload, form quality, consistency). 
                - Invite them to tell more about their likings and dislikes."""

            response = self._call_llm(system_prompt, user_prompt, max_tokens=100)
            
            return {
                "status": "success",
                "message": response
            }
            
        except Exception:
            return {
                "status": "error",
                "message": "Great! I've recorded your fitness goals."
            }

    def generate_workout(self, user_profile: UserProfile) -> Dict:
        """Third LLM call - generate detailed workout plan"""
        try:
            system_prompt = """You are Mylo, an expert strength & conditioning coach.

            Goal: Create a **complete, weekly workout plan** for the user based on their profile, goals, preferences, and available equipment.

            Tone & Style:
            - Sound natural and motivating, like a real coach.
            - Be clear and structured. Use markdown-style headers for each day and bullets under each.
            - Include rest days and active recovery days.
            - Adapt workouts to the user’s injuries, restrictions, and available equipment.
            - Recommend training split (e.g. upper/lower, push/pull/legs, full-body 3x/week) that best suits their goals and experience level.

            Each training day should include:
            - **Day Name/Focus** (e.g. “Day 1 – Lower Body Strength”)
            - **Warm-Up**
            - **Main Workout**: exercises with sets/reps + rest + brief coaching cues
            - **Cool-Down**
            - **Optional Modifications** (if applicable for injuries/equipment)

            Structure (use markdown format):
            # Weekly Workout Plan
            ## Overview
            - Days per week: <#>
            - Split type: <e.g. 4-day upper/lower>
            - Equipment: <list>

            ## Day 1 – <Title>
            - Warm-Up:
            - ...
            - Main Workout:
            - ...
            - Cool-Down:
            - ...

            (repeat for each day)

            ## Tips
            - Mention how the user should progress each week (e.g. increase reps, weight, or RPE)
            - Encourage consistency and recovery.

            If the user has specific injuries or no equipment, adapt accordingly.
            Avoid medical advice or hype.
            """
            
            # Build user context
            goals_text = ", ".join([goal.goal_type for goal in user_profile.goals])
            equipment_text = ", ".join(user_profile.restrictions.equipment) if user_profile.restrictions.equipment else "bodyweight only"
            workout_types_text = ", ".join(user_profile.preferences.preferred_workout_types) if user_profile.preferences.preferred_workout_types else "any type"
            
            user_prompt = f"""Build a complete weekly workout plan for this user:

            USER PROFILE:
            - Age: {user_profile.physical_stats.age}
            - Gender: {user_profile.physical_stats.gender}
            - Activity Level: {user_profile.activity_level}
            - Goals: {goals_text}
            - Available Equipment: {equipment_text}
            - Preferred Workout Types: {workout_types_text}
            - Injuries/Restrictions: {', '.join(user_profile.restrictions.injuries) if user_profile.restrictions.injuries else 'none'}

            
            Create a professional weekly workout split that’s safe, goal-aligned, and realistic for their profile. Make sure it includes rest or recovery days. Keep it structured but motivating — like a coach planning for a client."""

            response = self._call_llm(system_prompt, user_prompt, max_tokens=2000)
            
            return {
                "status": "success",
                "workout": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


