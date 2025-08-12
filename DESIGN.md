# Mylo - AI Fitness Coaching Chatbot
## Comprehensive Design Document

### 🎯 Project Overview
Mylo is an AI-powered fitness coaching chatbot that combines conversational AI with computer vision for comprehensive fitness guidance. This project progresses from prompt engineering (Phase 1) to fine-tuned models and computer vision integration (Future Phases).

---

## 🏗️ System Architecture

### Current Phase - Core Implementation
```
Frontend (React)               Backend (FastAPI)              Data Layer
┌─────────────────┐           ┌──────────────────┐           ┌─────────────────┐
│ Chat Interface  │ ←────────→ │ Conversation     │ ←────────→ │ MongoDB         │
│ User Profiles   │           │ Manager          │           │ - User Profiles │
│ Exercise Views  │           │                  │           │ - Conversations │
└─────────────────┘           │ RAG Pipeline     │           │ - Exercise Meta │
                              │ - Embeddings     │           └─────────────────┘
                              │ - Semantic Search│           
                              │                  │           ┌─────────────────┐
                              │ LLM Integration  │ ←────────→ │ Qdrant Vector   │
                              │ (HuggingFace)    │           │ Database        │
                              └──────────────────┘           │ - Exercise      │
                                                             │   Embeddings    │
                                                             └─────────────────┘
```

### Future Phase - Computer Vision Integration
```
┌─────────────────────────────────────────────────────────────────┐
│                        Extended System                          │
├─────────────────┬──────────────────┬─────────────────┬─────────┤  
│ Video Upload    │ MediaPipe        │ Form Analysis   │ LLM     │
│ Interface       │ Pose Detection   │ Engine          │ Feedback│
│                 │ - 33 Landmarks   │ - Joint Angles  │ Gen     │
│                 │ - Real-time      │ - Rule-based    │         │
└─────────────────┴──────────────────┴─────────────────┴─────────┘
```

---

## 🤖 Conversational AI System

### 3-Layer Questioning Approach

#### Layer 1 - Basic Introduction
- **Data Collection**: Name, body weight, height, body fat %, gender, age, prior experience
- **Personality**: Friendly introduction, welcoming tone
- **Storage**: User profile creation in MongoDB

#### Layer 2 - Goals Definition  
- **Options**: Fat loss, muscle gain (size/strength), maintenance, flexibility, endurance
- **Approach**: Interactive goal setting with Mylo's motivating commentary
- **Storage**: Goal preferences linked to user profile

#### Layer 3 - Activity Details
- **Comprehensive Data**: Injuries, body part focus, sleep patterns, work schedule, exercise preferences, available resources
- **Personalization**: Deep dive into user's specific situation
- **Storage**: Detailed activity profile for workout generation

### Personality System
- **Traits**: Friendly, funny, helpful, storytelling, motivating
- **Implementation**: 
  - System prompts defining Mylo's character
  - Few-shot examples for each conversation layer
  - Dynamic response generation based on user context

---

## 🔍 RAG Pipeline Architecture

### Exercise Database Schema
```python
{
    "exercise_id": "uuid",
    "name": "Push-up",
    "category": "bodyweight",
    "muscle_groups": ["chest", "triceps", "shoulders"],
    "equipment": "none",
    "difficulty": "beginner",
    "form_cues": [
        "Keep body in straight line",
        "Lower chest to ground",
        "Push through palms"
    ],
    "common_mistakes": ["Sagging hips", "Partial range of motion"],
    "variations": ["knee push-up", "diamond push-up"],
    "joint_angles": {  // For future CV integration
        "shoulder": {"min": 0, "max": 180},
        "elbow": {"min": 0, "max": 150}
    },
    "embedding": [0.1, 0.2, ...],  // 384-dimensional vector
    "created_at": "timestamp"
}
```

### Semantic Search Implementation
1. **Embedding Generation**: sentence-transformers (all-MiniLM-L6-v2)
2. **Vector Storage**: Qdrant for efficient similarity search
3. **Query Processing**: User goals → embeddings → similar exercises
4. **Context Injection**: Retrieved exercises + user profile → LLM prompts

### RAG Flow
```
User Query → Embedding → Qdrant Search → Context Assembly → LLM → Response
     ↑                                           ↓
User Profile ←─────────── MongoDB ──────────── Exercise Data
```

---

## 💻 Technical Stack

### Current Implementation
- **Frontend**: React 18 + Tailwind CSS + Shadcn/ui
- **Backend**: FastAPI (async) + Pydantic models
- **Database**: MongoDB (user data) + Qdrant (vectors)
- **LLM**: Hugging Face Inference API (free tier)
- **Embeddings**: sentence-transformers (local)
- **State Management**: React hooks + MongoDB persistence

### Dependencies
```python
# Backend
fastapi==0.104.1
sentence-transformers==2.2.2
qdrant-client==1.7.0
transformers==4.36.0
motor==3.3.2
httpx==0.25.2

# Frontend  
react==18.2.0
@radix-ui/react-*
tailwindcss==3.3.6
lucide-react==latest
```

---

## 🎯 Core Features Implementation

### 1. Conversation Management
```python
class ConversationState(BaseModel):
    user_id: str
    current_layer: int  # 1, 2, or 3
    layer_1_data: Optional[UserBasics]
    layer_2_data: Optional[UserGoals]  
    layer_3_data: Optional[UserDetails]
    conversation_history: List[Message]
    next_question: Optional[str]
```

### 2. Dynamic Prompt Construction
- **System Prompt**: Mylo's personality + current conversation context
- **Few-shot Examples**: Layer-specific conversation examples
- **User Context**: Profile data + conversation history
- **Exercise Context**: RAG-retrieved relevant exercises

### 3. Exercise Recommendation Engine
```python
async def get_exercise_recommendations(
    user_profile: UserProfile,
    query: str,
    limit: int = 5
) -> List[Exercise]:
    # Generate query embedding
    # Search Qdrant for similar exercises
    # Filter by user constraints (equipment, injuries)
    # Return personalized recommendations
```

---

## 🚀 Future Computer Vision Integration

### MediaPipe Pose Estimation
```python
class PoseAnalyzer:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        
    def analyze_form(self, video_frame):
        # Extract 33 pose landmarks
        # Calculate joint angles (knee, hip, ankle)
        # Apply rule-based validation
        # Generate feedback data
        
    def validate_squat_form(self, landmarks):
        # Knee angle analysis
        # Hip depth check  
        # Back straightness
        # Return form score + corrections
```

### Integration Points
1. **Video Upload**: Frontend component for exercise recording
2. **Real-time Analysis**: Frame-by-frame pose detection
3. **Form Validation**: Rule-based checking against exercise standards
4. **LLM Feedback**: Natural language generation from analysis results

---

## 📊 Data Models

### User Management
```python
class UserProfile(BaseModel):
    user_id: str
    name: str
    physical_stats: PhysicalStats
    goals: List[FitnessGoal]
    preferences: UserPreferences
    activity_level: str
    restrictions: List[str]  # injuries, equipment
    created_at: datetime
```

### Conversation Tracking
```python
class ConversationSession(BaseModel):
    session_id: str
    user_id: str
    messages: List[ChatMessage]
    current_state: ConversationState
    recommended_exercises: List[str]
    session_start: datetime
```

---

## 🔧 Development Phases

### Phase 1: Core Conversational AI ✅ (Current)
- [x] Basic chat interface
- [x] 3-layer questioning system
- [x] User profile management
- [x] RAG pipeline with exercise database
- [x] LLM integration (HuggingFace)
- [x] Semantic search with Qdrant

### Phase 2: Enhanced Intelligence
- [ ] Advanced conversation flow
- [ ] Workout plan generation
- [ ] Progress tracking
- [ ] Exercise instruction system

### Phase 3: Computer Vision Integration
- [ ] MediaPipe pose detection
- [ ] Real-time form analysis
- [ ] Video upload interface
- [ ] Form correction feedback

### Phase 4: Fine-tuning & Optimization
- [ ] Custom model fine-tuning
- [ ] Performance optimization
- [ ] Advanced personalization
- [ ] Multi-modal integration

---

## 🎨 UI/UX Design Principles

### Chat Interface
- **Modern Design**: Glass-morphism effects, smooth animations
- **Responsive Layout**: Mobile-first approach
- **Visual Feedback**: Typing indicators, message status
- **Exercise Visualization**: Cards with images and instructions

### User Experience Flow
1. **Onboarding**: Guided 3-layer introduction
2. **Dashboard**: Progress overview + quick chat access
3. **Exercise Library**: Searchable database with filters
4. **Chat Interface**: Primary interaction point with Mylo

---

## 🚦 Performance Considerations

### Scalability Features
- **Async Processing**: All backend operations async
- **Database Indexing**: Optimized queries for user data
- **Caching Strategy**: Exercise embeddings cached in memory
- **Connection Pooling**: MongoDB and Qdrant connections

### Future Optimizations
- **Message Queuing**: For video processing workloads
- **CDN Integration**: For exercise images/videos
- **Microservices**: Separate CV processing service
- **Load Balancing**: Multi-instance deployment

---

## 🔒 Security & Privacy

### Data Protection
- **User Consent**: Clear data usage policies
- **Data Minimization**: Only collect necessary information
- **Secure Storage**: Encrypted sensitive data
- **API Security**: Rate limiting and authentication

### Privacy Considerations
- **Local Processing**: Embeddings generated locally
- **Data Retention**: Configurable conversation history limits
- **User Control**: Profile deletion and data export options

---

## 📈 Success Metrics

### User Engagement
- **Conversation Completion**: % users completing all 3 layers
- **Session Duration**: Average chat session length
- **Return Rate**: Daily/weekly active users
- **Goal Achievement**: User progress tracking

### Technical Performance
- **Response Time**: < 2s for chat responses
- **Search Accuracy**: Relevant exercise recommendations
- **System Uptime**: 99.9% availability target
- **Embedding Quality**: Semantic search precision

---

## 🛠️ Development Guidelines

### Code Organization
```
backend/
├── models/          # Pydantic models
├── services/        # Business logic (conversation, RAG, LLM)
├── database/        # MongoDB and Qdrant clients
├── api/            # FastAPI routes
├── utils/          # Helper functions
└── config/         # Settings and environment

frontend/
├── components/     # React components
├── services/       # API calls and business logic
├── hooks/          # Custom React hooks
├── utils/          # Helper functions
└── assets/         # Images and static files
```

### Best Practices
- **Type Safety**: Full TypeScript/Pydantic typing
- **Error Handling**: Comprehensive error management
- **Testing**: Unit tests for core functionality
- **Documentation**: Inline comments and API docs
- **Version Control**: Feature branch workflow

---

## 🎯 Next Steps

### Immediate Actions
1. ✅ Set up core architecture
2. ✅ Implement basic chat interface  
3. ✅ Create exercise database with embeddings
4. ✅ Integrate RAG pipeline
5. ✅ Deploy basic conversational flow

### Upcoming Milestones
1. **Enhanced Conversations**: Advanced prompt engineering
2. **Workout Generation**: Personalized routine creation
3. **Progress Tracking**: User journey analytics
4. **CV Preparation**: Data models for pose analysis

---

*This design document serves as the blueprint for Mylo's development, ensuring scalable architecture and clear implementation pathways for both current and future features.*


NOTES:
Template-based prompt construction for consistency
Context-aware prompt building based on user data
Modular prompt components for reusability