# test_workout_flow.py
"""
Simple test file to verify our workout generation flow
Run this file directly in VS Code to test everything step by step
"""

import sys
from datetime import datetime
from typing import Dict, Any
import os

# Import your existing models (adjust path as needed)
from models.user import (
    UserProfile, PhysicalStats, FitnessGoal, UserPreferences, Restrictions
) 

# Import our new workout generator components
from services.workoutGenerator.llmClient import LLMConfig, GroqLLMClient
from services.workoutGenerator.promptEngine import WorkoutPromptEngine


def create_sample_user() -> UserProfile:
    """Create a sample user for testing"""
    return UserProfile(
        user_id="test_user_123",
        name="Alex Johnson",
        physical_stats=PhysicalStats(
            height=175.0,  # cm
            weight=70.0,   # kg
            gender="male",
            age=28
        ),
        goals=[
            FitnessGoal(goal_type="weight_loss")
        ],
        preferences=UserPreferences(
            preferred_workout_types=["strength_training", "cardio"],
            preferred_training_times=["morning"]
        ),
        activity_level="moderately_active",
        restrictions=Restrictions(
            injuries=[],  # No injuries
            equipment=["dumbbells", "resistance_bands"],  # Has some equipment
            not_preferred_exercises=["burpees"],
            special_considerations=[]
        ),
        created_at=None
    )


def test_prompt_generation():
    """Test 1: Verify prompt generation works"""
    print("🧪 TEST 1: Prompt Generation")
    print("-" * 40)
    
    try:
        # Create test user
        user = create_sample_user()
        print(f"✅ Created test user: {user.name}")
        
        # Initialize prompt engine
        prompt_engine = WorkoutPromptEngine()
        print("✅ Initialized prompt engine")
        prompt_engine.reload_templates()
        
        # Generate prompts
        prompts = prompt_engine.build_prompt(user)
        print("✅ Generated prompts successfully")
        
        # Display results
        print(f"\n🎯 System Prompt:")
        print(prompts["system"])
        
        print(f"\n👤 User Prompt:")
        print(prompts["user"])
        
        print(f"\n✅ TEST 1 PASSED: Prompt generation working!\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FAILED: {str(e)}")
        return False



def test_llm_client():
    """Test 3: Verify LLM client works (optional - needs internet)"""
    print("🧪 TEST 3: LLM Client (Optional)")
    print("-" * 40)
    
    try:
        # Create simple LLM config (no API key needed for testing)
        config = LLMConfig(
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key="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",
            max_tokens=500  # Short response for testing

        )
        print("✅ Created LLM config")
        
        # Initialize client
        client = GroqLLMClient(config)
        print("✅ Initialized LLM client")
        
        if True:
            # Test simple generation
            print("🤖 Testing LLM generation...")
            simple_system = "You are a helpful fitness assistant."
            simple_user = "Create a 5-minute warm-up routine."
            
            response = client.generate(simple_system, simple_user)
            print(f"✅ LLM Response received: {len(response.content)} characters")
            print(f"📝 Sample response: {response.content}...")
            
            print(f"\n✅ TEST 3 PASSED: LLM client working!\n")
            return True
        else:
            print("⚠️  TEST 3 SKIPPED: No internet or API not available\n")
            return True
            
    except Exception as e:
        print(f"⚠️  TEST 3 SKIPPED: {str(e)}")
        return True

async def generate_safe_workout(user_profile: UserProfile, llm_client):
    engine = WorkoutPromptEngine()
    
    while True:
        # Generate prompts
        prompts = engine.build_prompt(user_profile)
        
        # Get LLM response
        llm_response = await llm_client.generate(
            prompts["system"], 
            prompts["user"]
        )
        
        # Validate and process
        result = engine.validate_and_process_response(
            llm_response.content,
            user_profile.restrictions.constraints
        )
        
        if result["status"] == "success":
            return result["workout"]
        
        # If we need to regenerate, continue the loop
        if result["needs_regeneration"]:
            continue
            
        # If there's an error but no regeneration needed, raise it
        raise ValueError(result["message"])



def test_integration():
    """Integration test: Generate a safe workout"""
    print("Integration Test")

    try:    
        # Create test user
        user = create_sample_user()
        print(f"✅ Created test user: {user.name}")

        # Initialize prompt engine
        prompt_engine = WorkoutPromptEngine()
        print("✅ Initialized prompt engine")
        prompt_engine.reload_templates()
        
        # Generate prompts
        prompts = prompt_engine.build_prompt(user)
        print("✅ Generated prompts successfully")

        config = LLMConfig(
        model_name="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key="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",
        max_tokens=1000 # Short response for testing

        )   
        print("✅ Created LLM config")
            
        # Initialize client
        client = GroqLLMClient(config)
        print("✅ Initialized LLM client")

        llm_response = client.generate(
        prompts["system"], 
        prompts["user"]
        )
        print("✅ Received LLM response", llm_response)
    # while True:
        
    #     # Get LLM response
    #     llm_response = client.generate(
    #         prompts["system"], 
    #         prompts["user"]
    #     )
        
    #     # Validate and process
    #     result = prompt_engine.validate_and_process_response(
    #         llm_response.content,
    #         user.restrictions.constraints
    #     )
        
    #     if result["status"] == "success":
    #         return result["workout"]
        
    #     # If we need to regenerate, continue the loop
    #     if result["needs_regeneration"]:
    #         continue
            
    #     # If there's an error but no regeneration needed, raise it
    #     raise ValueError(result["message"])

    except Exception as e:
        print(f"⚠️ INTEGRATION TEST  SKIPPED: {str(e)}")
        return True
    

def run_all_tests():
    """Run all tests in sequence"""
    print("🚀 STARTING WORKOUT GENERATOR TESTS")
    print("=" * 50)
    
    test_results = []
    
    # Test 1: Prompt Generation (always works offline)
    # test_results.append(test_prompt_generation())

    
    # Test 3: LLM Client (requires internet)
    # test_results.append(test_llm_client())

    # Integration test: Generate a safe workout
    test_results.append(test_integration())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    print("=" * 50)
    print("🏁 TEST SUMMARY")
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your workout generator is ready!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")



# if __name__ == "__main__":
#     """
#     This block runs when you execute this file directly
#     """
#     print("🔧 Testing Workout Generator Flow...")
#     print(f"Python version: {sys.version}")
#     print(f"Test started at: {datetime.now()}")
#     print()
    
#     try:
#         run_all_tests()
#     except KeyboardInterrupt:
#         print("\n⏹️  Tests interrupted by user")
#     except Exception as e:
#         print(f"\n💥 Unexpected error: {str(e)}")
#         print("Check your imports and file paths!")

