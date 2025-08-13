from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Production-ready configuration
MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mylo")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
