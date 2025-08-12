# mylo_ai_fitness/models/llm.py
from typing import Dict, Optional
from pydantic import BaseModel

class LLMConfig(BaseModel):
    """Configuration for LLM client"""
    provider: str = "groq"
    model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct"  # Better default model
    api_key: Optional[str] = None  # Optional for public models
    base_url: str = "https://api.groq.com/openai/v1/chat/completions"
    max_tokens: int = 1000
    temperature: float = 0.3
    timeout: int = 30



class LLMResponse(BaseModel):
    """Standardized LLM response"""
    content: str
    model_used: str
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    raw_response: Optional[Dict] = None