from fastapi import FastAPI, HTTPException
from services.orchestrator import WorkoutOrchestrator
from fastapi.middleware.cors import CORSMiddleware 
from models.user import FitnessGoal, PhysicalStats, Restrictions, UserPreferences, UserProfile

app = FastAPI(title="Mylo AI Fitness", description="AI-powered workout generation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

orchestrator = WorkoutOrchestrator()


def create_sample_user() -> UserProfile:
    """Create a sample user for testing"""
    return UserProfile(
        user_id="test_user_123",
        name="Koyel Das",
        physical_stats=PhysicalStats(
            height=164.0,  # cm
            weight=80.0,   # kg
            gender="female",
            age=30
        ),
        goals=[
            FitnessGoal(goal_type="weight_loss")
        ],
        preferences=UserPreferences(
            preferred_workout_types=["strength_training", "cardio", "pilates"],
            preferred_training_times=["evening"]
        ),
        activity_level="moderately_active",
        restrictions=Restrictions(
            injuries=[],  # No injuries
            equipment=[],  # Has some equipment
            not_preferred_exercises=["lunges"],
            special_considerations=[]
        ),
        created_at=None
    )


@app.options("/generate-workout")
async def options_generate_workout():
    """Handle CORS preflight requests"""
    return {}

@app.post("/generate-workout")
async def generate_workout(user: UserProfile):
    """Generate a personalized workout for the user"""
    try:
        result = orchestrator.generate_workout(user)
        
        if result["status"] == "success":
            return {
                "status": "success",
                "workout": result["workout"],
                "raw_workout": result["raw_workout"]
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Workout generation failed: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Mylo AI Fitness API is running!"}


# CLI usage example
def main():
    # Create a sample user
    user = create_sample_user()  # Your user data here
    
    # Generate workout
    orchestrator = WorkoutOrchestrator()
    result = orchestrator.generate_workout(user)
    
    if result["status"] == "success":
        print(result["workout"])  # Prints nicely formatted workout
    else:
        print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()