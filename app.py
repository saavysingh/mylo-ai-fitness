from fastapi import FastAPI, HTTPException
from services.orchestrator import WorkoutOrchestrator
from fastapi.middleware.cors import CORSMiddleware 
from models.user import FitnessGoal, PhysicalStats, Restrictions, UserPreferences, UserProfile
from models.schemas import (
    ChatIn, ChatOut, ChatStage, ConversationState, Basics, GoalBlock, PrefsConstraints,
    GENDER, ACTIVITY, GOALS, EQUIPMENT, WORKOUT_TYPES, TIMES
)
import uuid

app = FastAPI(title="Mylo AI Fitness", description="AI-powered workout generation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

orchestrator = WorkoutOrchestrator()


def create_user_profile(state: ConversationState) -> UserProfile:
    """Create a UserProfile from conversation state"""
    return UserProfile(
        user_id=state.session_id,
        name=state.basics.name or "User",
        physical_stats=PhysicalStats(
            height=state.basics.height_cm,
            weight=state.basics.weight_kg,
            gender=state.basics.gender,
            age=state.basics.age
        ),
        goals=[FitnessGoal(goal_type=goal) for goal in state.goals_block.goals],
        preferences=UserPreferences(
            preferred_workout_types=state.prefs.preferred_workout_types,
            preferred_training_times=state.prefs.preferred_training_times
        ),
        activity_level=state.basics.activity_level,
        restrictions=Restrictions(
            injuries=state.prefs.injuries,
            equipment=state.prefs.equipment,
            not_preferred_exercises=state.prefs.not_preferred_exercises,
            special_considerations=state.prefs.special_considerations
        ),
        created_at=None
    )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Mylo AI Fitness API is running!"}


def get_or_create_state(session_id: str, stage: ChatStage) -> ConversationState:
    """Get existing conversation state or create new one"""
    if not hasattr(app, 'conversation_states'):
        app.conversation_states = {}
    
    state = app.conversation_states.get(session_id)
    if not state:
        state = ConversationState(
            session_id=session_id or str(uuid.uuid4()),
            stage=stage,
            missing=[]
        )
        app.conversation_states[state.session_id] = state
    
    state.stage = stage
    return state

@app.post("/chat/ingest")
async def chat_ingest(chat_in: ChatIn) -> ChatOut:
    """Handle the 3-step chat intake process"""
    state = get_or_create_state(chat_in.session_id, chat_in.stage)
    assistant_text = ""
    next_stage = chat_in.stage
    controls = {}

    if chat_in.stage == ChatStage.BASIC:
        # Handle basic information intake
        if chat_in.selections:
            state.basics = Basics(**chat_in.selections)
            missing = []
            for field in ["age", "gender", "height_cm", "weight_kg", "activity_level"]:
                if not getattr(state.basics, field):
                    missing.append(field)
            state.missing = missing

            if not missing:
                # Get personalized response from LLM
                llm_response = orchestrator.analyze_basic_info(state.basics)
                if llm_response["status"] == "success":
                    assistant_text = llm_response["message"]
                else:
                    assistant_text = "Thanks! I've recorded your basic information."
                
                next_stage = ChatStage.GOALS
                controls = {"available_goals": GOALS}
            else:
                assistant_text = f"I still need a few details from you: {', '.join(missing)}. This helps me create the perfect plan for you!"
        else:
            assistant_text = "Hi! I'm Mylo, your AI fitness coach. To create a personalized plan for you, I'll need some basic information. Let's start with your age, gender, height, weight, and activity level."
            controls = {
                "required_fields": ["age", "gender", "height_cm", "weight_kg", "activity_level"],
                "options": {
                    "gender": GENDER,
                    "activity_level": ACTIVITY
                }
            }

    elif chat_in.stage == ChatStage.GOALS:
        # Handle goals intake
        if not state.basics:
            raise HTTPException(status_code=400, detail="Basic information must be provided first")
        
        if chat_in.selections:
            state.goals_block = GoalBlock(**chat_in.selections)
            if not state.goals_block.goals:
                assistant_text = "I'd love to help you achieve your fitness goals! Please select at least one goal that resonates with you."
                controls = {"available_goals": GOALS}
            else:
                # Get personalized response from LLM
                llm_response = orchestrator.analyze_goals(state.basics, state.goals_block)
                if llm_response["status"] == "success":
                    assistant_text = llm_response["message"]
                else:
                    assistant_text = "Great! I've recorded your fitness goals."
                
                next_stage = ChatStage.FINAL
                controls = {
                    "equipment": EQUIPMENT,
                    "workout_types": WORKOUT_TYPES,
                    "training_times": TIMES
                }
        else:
            assistant_text = "Now that I know a bit about you, I'd love to understand your fitness goals. What would you like to achieve? You can select multiple goals!"
            controls = {"available_goals": GOALS}

    elif chat_in.stage == ChatStage.FINAL:
        # Handle preferences and constraints
        if not state.basics or not state.goals_block:
            raise HTTPException(status_code=400, detail="Basic information and goals must be provided first")
        
        if chat_in.selections:
            state.prefs = PrefsConstraints(**chat_in.selections)
            assistant_text = "Perfect! Now I have everything I need to create a personalized workout plan that's just right for you. Give me a moment while I design something special..."
            
            # Convert state to UserProfile for workout generation
            user_profile = create_user_profile(state)
            
            # Generate workout using existing orchestrator
            workout_result = orchestrator.generate_workout(user_profile)
            if workout_result["status"] == "success":
                controls = {"workout": workout_result["workout"]}
            else:
                raise HTTPException(status_code=400, detail=workout_result["message"])
        else:
            assistant_text = "Almost done! Please provide your workout preferences and any constraints."
            controls = {
                "equipment": EQUIPMENT,
                "workout_types": WORKOUT_TYPES,
                "training_times": TIMES
            }

    return ChatOut(
        assistant_text=assistant_text,
        state=state,
        next_stage=next_stage,
        controls=controls
    )

