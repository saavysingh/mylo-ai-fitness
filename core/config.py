from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

MONGO_URL   = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME     = os.getenv("DB_NAME", "mylo")
MODEL_NAME  = os.getenv("MODEL_NAME", "google/flan-t5-large")  # open-source T5
GROQ_API_KEY="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"
