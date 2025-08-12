# mylo_ai_fitness/services/workoutGenerator/promptEngine.py
import yaml
from typing import Dict, List
from jinja2 import Template
from pathlib import Path
import os

from models.user import UserProfile, FitnessGoal, UserPreferences, Restrictions
from models.prompt import PromptContext, PromptTemplate
from services.workoutGenerator.workoutPostProcessor import WorkoutPostProcessor

class WorkoutPromptEngine():
    """
    Production prompt engine for workout generation
    
    Features:
    - Dynamic context analysis
    - Template-based prompt construction
    - Constraint-aware prompt building
    """
    
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = os.path.join(
                os.path.dirname(__file__), 
                'templates'
            )
        self.templates_dir = Path(templates_dir)
        self.templates = self._initialize_templates()
    
    def build_prompt(self, user_profile: UserProfile) -> Dict[str, str]:
        """
        Build dynamic prompt from user profile
        
        Returns:
            Dict with 'system' and 'user' prompt components
        """
        # 1. Analyze user context
        context = self._analyze_user_context(user_profile)
        
        # 2. Select appropriate template
        template = self._select_template(context)
        
        # 3. Build dynamic prompt
        prompts = self._construct_prompts(template, context)
        
        return prompts
    
    def _analyze_user_context(self, user_profile: UserProfile) -> PromptContext:
        """
        Analyze user profile and create structured context
        
        This is where we transform raw user data into prompt-ready context
        """
        # Extract primary goal
        primary_goal = user_profile.goals[0].goal_type if user_profile.goals else "general_fitness"
        
        # Determine experience level
        experience_level = self._determine_experience_level(user_profile)
        
        # Extract constraints
        constraints = []
        if user_profile.restrictions.injuries:
            constraints.extend([f"Has {injury} injury" for injury in user_profile.restrictions.injuries])
        if user_profile.restrictions.equipment:
            equipment_str = ", ".join(user_profile.restrictions.equipment)
            constraints.append(f"Available equipment: {equipment_str}")
        else:
            constraints.append("No equipment available (bodyweight only)")
        if user_profile.restrictions.not_preferred_exercises:
            not_preferred = ", ".join(user_profile.restrictions.not_preferred_exercises)
            constraints.append(f"Not preferred exercises: {not_preferred}")
        if user_profile.restrictions.special_considerations:
            considerations = ", ".join(user_profile.restrictions.special_considerations)
            constraints.append(f"Special considerations: {considerations}")
        
        # Extract preferences
        preferences = []
        if user_profile.preferences.preferred_workout_types:
            workout_types = ", ".join(user_profile.preferences.preferred_workout_types)
            preferences.append(f"Prefers: {workout_types}")
        if user_profile.preferences.preferred_training_times:
            times = ", ".join(user_profile.preferences.preferred_training_times)
            preferences.append(f"Trains: {times}")
        
        return PromptContext(
            user_basics={
                "name": user_profile.name,
                "age": user_profile.physical_stats.age,
                "gender": user_profile.physical_stats.gender,
                "activity_level": user_profile.activity_level
            },
            goals_summary=self._create_goals_summary(user_profile.goals),
            experience_level=experience_level,
            constraints=constraints,
            preferences=preferences,
            workout_focus=primary_goal,
            estimated_duration=self._estimate_workout_duration(user_profile)
        )
    
    def _determine_experience_level(self, user_profile: UserProfile) -> str:
        """Simple experience level determination"""
        activity_mapping = {
            "sedentary": "beginner",
            "lightly_active": "beginner", 
            "moderately_active": "intermediate",
            "very_active": "intermediate",
            "extremely_active": "advanced"
        }
        return activity_mapping.get(user_profile.activity_level, "beginner")
    
    def _create_goals_summary(self, goals: List[FitnessGoal]) -> str:
        """Create human-readable goals summary"""
        if not goals:
            return "general fitness and health"
        
        goal_descriptions = {
            "weight_loss": "lose weight and improve body composition",
            "muscle_gain": "build muscle mass and strength", 
            "endurance": "improve cardiovascular endurance",
            "strength": "increase overall strength",
            "flexibility": "improve flexibility and mobility"
        }
        
        goal_texts = [goal_descriptions.get(goal.goal_type, goal.goal_type) for goal in goals]
        return ", ".join(goal_texts)
    
    def _estimate_workout_duration(self, user_profile: UserProfile) -> str:
        """Estimate appropriate workout duration"""
        experience_mapping = {
            "beginner": "30-45 minutes",
            "intermediate": "45-60 minutes", 
            "advanced": "50-65 minutes"
        }
        experience = self._determine_experience_level(user_profile)
        return experience_mapping.get(experience, "30-45 minutes")
    
    
    def _construct_prompts(self, template: PromptTemplate, context: PromptContext) -> Dict[str, str]:
        """Construct final prompts using template and context"""
        
        # Build user prompt from template
        user_template = Template(template.user_prompt_template)
        user_prompt = user_template.render(
            name=context.user_basics["name"],
            age=context.user_basics["age"],
            gender=context.user_basics["gender"],
            activity_level=context.user_basics["activity_level"],
            goals=context.goals_summary,
            experience=context.experience_level,
            constraints=context.constraints,
            preferences=context.preferences,
            duration=context.estimated_duration,
            focus=context.workout_focus
        )
        
        return {
            "system": template.system_prompt,
            "user": user_prompt,
            "expected_format": template.expected_format
        }
    
    def _initialize_templates(self) -> Dict[str, PromptTemplate]:
        """Initialize prompt templates from YAML files"""
        templates = {}
        
        # Load all YAML files from templates directory
        for template_file in self.templates_dir.glob('*.yaml'):
            try:
                with open(template_file, 'r') as f:
                    template_data = yaml.safe_load(f)
                    
                templates[template_data['name']] = PromptTemplate(
                    name=template_data['name'],
                    system_prompt=template_data['system_prompt'],
                    user_prompt_template=template_data['user_prompt_template'],
                    expected_format=template_data['expected_format'],
                    example_output=template_data.get('example_output', '')
                )
            except Exception as e:
                print(f"Error loading template {template_file}: {str(e)}")
                continue
        
        if not templates:
            raise ValueError(
                f"No templates found in {self.templates_dir}"
            )
        
        return templates
    
    def _select_template(self, context: PromptContext) -> PromptTemplate:
        """Select appropriate template based on context"""
        # For now, just return the main template
        # TODO: Implement smart template selection based on context
        return self.templates['main_workout']
    
    # Add this method to WorkoutPromptEngine class
    def reload_templates(self):
        """Reload templates from files"""
        self.templates = self._initialize_templates()

    def validate_and_process_response(
        self, 
        llm_response: str, 
        constraints: List[str]
    ) -> Dict:
        """
        Validates and processes the LLM response
        """
        workout_post_processor = WorkoutPostProcessor()
        is_valid, workout, error = workout_post_processor.process_workout(
            llm_response, constraints
        )
        
        if not is_valid:
            return {
                "status": "error",
                "message": error,
                "needs_regeneration": True
            }
        
        return {
            "status": "success",
            "workout": workout.dict(),
            "needs_regeneration": False
        }


