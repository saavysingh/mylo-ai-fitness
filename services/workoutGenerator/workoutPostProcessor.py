import json
from typing import Dict, List, Optional
from models.workout import WorkoutPlan
import re


def extract_and_repair_json(text: str) -> str:
    """
    Extracts JSON from LLM output and attempts minor repairs to make it valid.
    Returns a JSON string.
    """
    # 1. Remove markdown code fences if present
    text = re.sub(r"^```(json)?", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"```$", "", text.strip(), flags=re.MULTILINE)

    # 2. Extract the first {...} block in case there's extra text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    # 3. Basic repairs for common issues
    # Remove trailing commas before closing braces/brackets
    text = re.sub(r",(\s*[}\]])", r"\1", text)

    # Replace smart quotes with normal quotes
    text = text.replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")

    # 4. Validate and pretty-print JSON
    try:
        obj = json.loads(text)
        return json.dumps(obj, indent=2)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not repair JSON: {e}\nRaw text: {text[:200]}...")

class WorkoutPostProcessor:
    """Post-processes and validates LLM-generated workouts"""
    
    
    def process_workout(
        self, 
        workout_json: str, 
    ) -> tuple[bool, Optional[WorkoutPlan], Optional[str]]:
        """
        Processes and validates a workout
        
        Returns:
            Tuple of (is_valid, workout_plan, error_message)
        """

        try:
            possible_json = json.loads(workout_json)
            if isinstance(possible_json, str):
                workout_dict = json.loads(possible_json)  # string inside string
            else:
                workout_dict = possible_json
        except json.JSONDecodeError:
            try:
                workout_dict = json.loads(extract_and_repair_json(workout_json))
            except (json.JSONDecodeError, ValueError) as e:
                return False, None, f"Invalid JSON format: {str(e)}"
        
        try:
            # 3. Validate against schema
            workout = WorkoutPlan(**workout_dict)
            
            # 4. Safety checks removed - just return success
            return True, workout, None
            
        except ValueError as e:
            return False, None, f"Schema validation error: {str(e)}"
    