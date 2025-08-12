from typing import Dict
import logging

from models.user import UserProfile
from services.workoutGenerator.workoutPostProcessor import WorkoutPostProcessor
from services.workoutGenerator.promptEngine import WorkoutPromptEngine
from services.workoutGenerator.llmClient import GroqLLMClient, LLMConfig
from core.config import GROQ_API_KEY

class WorkoutOrchestrator:
    """
    Orchestrates the end-to-end workflow for workout generation:
    1. Load user profile
    2. Generate workout using LLM
    3. Validate and process response
    4. Format for display
    5. Save to history (optional)
    """
    
    def __init__(self):
        self.prompt_engine = WorkoutPromptEngine()
        self.llm_client = GroqLLMClient(
            config=LLMConfig(
                model_name="meta-llama/llama-4-scout-17b-16e-instruct",
                api_key=GROQ_API_KEY,
                max_tokens=1000
            )
        )
        self.logger = logging.getLogger(__name__)


    
    def generate_workout(
        self, 
        user_profile: UserProfile,
    ) -> Dict:
        """
        Main workflow to generate a validated workout for a user
        """
        try:
            # 1. Generate prompts
            self.prompt_engine.reload_templates()
            prompts = self.prompt_engine.build_prompt(user_profile)
            self.logger.info(f"Generated prompts for user: {user_profile.name}")
            
            # Get LLM response
            llm_response = self.llm_client.generate(
                prompts["system"],
                prompts["user"]
            )
            
            # Validate and process
            workout_post_processor = WorkoutPostProcessor()
            is_valid, workout, error = workout_post_processor.process_workout(
                llm_response.content
            )
            
            if is_valid and workout:
                # Format the workout for display
                formatted_workout = self._format_workout(workout.dict())
                
                return {
                    "status": "success",
                    "workout": formatted_workout,
                    "raw_workout": workout.dict()
                }
            else:
                return {
                    "status": "error",
                    "message": error or "Failed to process workout"
                }
            
        except Exception as e:
            self.logger.error(f"Workout generation failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _format_workout(self, workout_data: dict) -> str:
        """Format workout data for user display"""
        output = []
        
        # Header
        output.append(f"🏋️‍♂️ {workout_data['title'].upper()}")
        output.append(f"📝 {workout_data['description']}\n")
        output.append(f"⏱️ Duration: {workout_data['total_duration']}")
        output.append(f"💪 Level: {workout_data['difficulty'].title()}\n")
        
        # Sections
        for section in workout_data['sections']:
            output.append(f"\n== {section['name'].upper()} ==")
            output.append(f"Duration: {section['duration']}\n")
            
            for i, exercise in enumerate(section['exercises'], 1):
                output.append(f"{i}. {exercise['name']}")
                output.append(f"   ⏱️ {exercise['duration']}")
                output.append(f"   📋 {exercise['instructions']}")
                if exercise['modifications']:
                    output.append(f"   🔄 {exercise['modifications']}")
                output.append("")
        
        # Footer
        if workout_data['notes']:
            output.append("📌 NOTES:")
            for note in workout_data['notes']:
                output.append(f"• {note}")
            output.append("")
        
        output.append("🎯 PROGRESSION PLAN:")
        output.append(workout_data['progression'])
        
        return "\n".join(output)


