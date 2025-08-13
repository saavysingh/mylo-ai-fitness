# Mylo AI Fitness - Simplified 🏋️‍♂️

A clean, simplified AI fitness assistant that generates personalized workout plans through a 3-step conversation flow.

## 🎯 Architecture

**Simple 3-Step Workflow:**
1. **Basic Info** → Concise LLM response
2. **Goals** → Concise LLM response  
3. **Preferences** → Detailed workout generation

## 🚀 Tech Stack

**Backend:**
- FastAPI (Python)
- Groq LLM API (Llama 3.1)
- Simple HTTP requests (no complex clients)

**Frontend:**
- React 18
- Tailwind CSS
- Single consolidated chat interface

## 📁 Project Structure

```
mylo_ai_fitness/
├── app.py                 # Main FastAPI app
├── services/
│   └── orchestrator.py    # Simple 3-step LLM workflow
├── models/
│   ├── schemas.py         # Pydantic models
│   └── user.py           # User profile models
├── core/
│   └── config.py         # Configuration
└── frontend/
    └── src/
        ├── App.jsx       # Simplified main app
        └── components/
            └── Chat/
                ├── ChatContainer.jsx  # All-in-one chat + forms
                └── ChatMessage.jsx    # Message display
```

## 🔧 Key Simplifications Made

### Backend Simplifications:
- ✅ Removed complex WorkoutGenerator with YAML templates
- ✅ Removed unused ConversationManager 
- ✅ Simplified orchestrator to direct LLM calls
- ✅ Consolidated model files
- ✅ Removed complex post-processing

### Frontend Simplifications:
- ✅ Removed sidebar navigation
- ✅ Consolidated 3 separate forms into single component
- ✅ Streamlined state management
- ✅ Simplified UI to focus on core workflow

## 🏃‍♂️ Quick Start

### Backend
```bash
cd mylo_ai_fitness
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🎨 User Experience

1. **Step 1:** User enters basic info (age, gender, height, weight, activity level)
2. **Step 2:** User selects fitness goals (weight loss, muscle gain, etc.)
3. **Step 3:** User sets preferences (equipment, workout types, timing)
4. **Result:** AI generates personalized workout plan

## 🚀 Deployment

- **Backend:** Deployed on Render
- **Frontend:** Deployed on Vercel

## 🧹 What Was Removed

- Complex YAML template system
- RAG pipeline and vector databases
- Multiple model classes
- Conversation state management complexity
- Sidebar navigation
- Separate form components
- Complex workout post-processing
- Unused test files and documentation

The result is a clean, maintainable codebase focused on delivering the core value: personalized workout generation through simple conversation.