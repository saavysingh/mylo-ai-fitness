# mylo_ai_fitness/services/workoutGenerator/llmClient.py
import requests
import time
import logging

from models.llm import LLMConfig, LLMResponse

logger = logging.getLogger(__name__)


class GroqLLMClient():

    def __init__(self, config: LLMConfig):
        self.config = config
        self.headers = {
            "Content-Type": "application/json"
        }
        if config.api_key:
            self.headers["Authorization"] = f"Bearer {config.api_key}"
    
    def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:

        start_time = time.time()
        
        try:
            # Combine prompts for models that don't support system/user separation
            
            url = f"{self.config.base_url}"
            
            # Prepare payload
            payload = {
                "model": self.config.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            }
            
            response_time = time.time() - start_time
            # Make the API call
            response = requests.post(
                url, 
                json=payload, 
                headers=self.headers, 
                timeout=self.config.timeout
            )
            
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result["choices"][0]["message"]["content"]
                
                return LLMResponse(
                    content=generated_text,
                    model_used=self.config.model_name,
                    response_time=response_time,
                    raw_response=result
                )
            else:
                logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return self._fallback_response(user_prompt)
                
        except requests.exceptions.Timeout:
            logger.error("Groq API timeout")
            return self._fallback_response(user_prompt)
        except requests.exceptions.RequestException as e:
            logger.error(f"Groq API request failed: {str(e)}")
            return self._fallback_response(user_prompt)
        except Exception as e:
            logger.error(f"Unexpected error in Groq LLM generation: {str(e)}")
            return self._fallback_response(user_prompt)
        
    
    def _fallback_response(self, user_prompt: str) -> LLMResponse:
        """Fallback response when LLM fails"""
        
        # Try to give a contextual fallback based on the prompt
        if "warm" in user_prompt.lower():
            fallback_content = """
## Warm-up Routine (5-10 minutes)
- Arm circles: 10 forward, 10 backward
- Leg swings: 10 each leg
- Torso twists: 10 each side
- Light marching in place: 1 minute
- Gentle stretching
            """.strip()
        elif "cool" in user_prompt.lower() or "stretch" in user_prompt.lower():
            fallback_content = """
## Cool-down Routine (5-10 minutes)
- Deep breathing: 1 minute
- Hamstring stretch: 30 seconds each leg
- Quad stretch: 30 seconds each leg
- Shoulder stretch: 30 seconds each arm
- Gentle spinal twist: 30 seconds each side
            """.strip()
        else:
            fallback_content = """
## Basic Workout Plan

**Warm-up (5 minutes)**
- Light cardio movements
- Dynamic stretching

**Main Workout (20 minutes)**
- Bodyweight squats: 3 sets of 10-15
- Push-ups (modified if needed): 3 sets of 8-12
- Plank hold: 3 sets of 20-30 seconds
- Walking or marching: 5 minutes

**Cool-down (5 minutes)**
- Static stretching
- Deep breathing exercises

*Note: This is a basic fallback workout. Adjust intensity based on your fitness level.*
            """.strip()
        
        return LLMResponse(
            content=fallback_content,
            model_used="fallback_template",
            response_time=0.1,
            raw_response={"fallback": True, "reason": "LLM_unavailable"}
        )

