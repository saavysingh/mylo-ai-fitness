from __future__ import annotations

import json
import tempfile
from pathlib import Path
import os
from typing import Dict, List, Tuple

from fastapi import HTTPException

from core.config import GROQ_API_KEY


_whisper_model = None
_CACHE_DIR = (Path(__file__).parent.parent / "model_cache" / "faster_whisper").resolve()
_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _get_whisper_model():
    """Lazy-load a singleton faster-whisper model to avoid cold starts per request."""
    global _whisper_model
    if _whisper_model is None:
        try:
            # Import here so the app can still run even if dependency isn't installed yet
            from faster_whisper import WhisperModel  # type: ignore
        except Exception as exc:  # pragma: no cover - dependency missing
            raise HTTPException(status_code=500, detail=f"Transcription backend not available: {exc}")

        # Use a small model for low latency on CPU by default; allow override via env
        model_size = os.getenv("WHISPER_MODEL_SIZE", "tiny.en")
        cpu_threads = int(os.getenv("WHISPER_THREADS", "4"))
        _whisper_model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
            download_root=str(_CACHE_DIR),
            cpu_threads=cpu_threads,
        )
    return _whisper_model


def transcribe_audio_to_text(file_path: Path) -> str:
    """Transcribe an audio file to text using faster-whisper.

    Args:
        file_path: path to audio file
    Returns:
        transcript string (may be empty if nothing recognized)
    """
    model = _get_whisper_model()
    try:
        segments, info = model.transcribe(
            str(file_path),
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
            beam_size=1,
            temperature=0.0,
        )
        transcript_parts: List[str] = [seg.text.strip() for seg in segments if seg.text]
        return " ".join(transcript_parts).strip()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {exc}")


def _call_groq_json(system_prompt: str, user_prompt: str) -> Dict:
    """Call Groq LLM and expect a compact JSON object in the response."""
    import requests

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 400,
                "temperature": 0.0,
            },
            timeout=30,
        )
        content = response.json()["choices"][0]["message"]["content"].strip()
        # Extract JSON from content (model should return pure JSON)
        # Fallback: find first '{' ... last '}'
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1:
                return json.loads(content[start : end + 1])
            raise HTTPException(status_code=500, detail="LLM did not return valid JSON")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {exc}")


def _schema_for_stage(stage: str) -> Tuple[str, List[str]]:
    """Return a JSON schema snippet and required field list for the stage."""
    stage = stage.lower()
    if stage == "basic":
        schema = (
            '{"name": string|null, "age": int|null, '
            '"gender": "male"|"female"|"other"|"prefer_not_to_say"|null, '
            '"height_cm": number|null, "weight_kg": number|null, '
            '"activity_level": "sedentary"|"lightly_active"|"moderately_active"|"very_active"|"extremely_active"|null}'
        )
        required = ["age", "gender", "height_cm", "weight_kg", "activity_level"]
        return schema, required
    if stage == "goals":
        schema = '{"goals": ("weight_loss"|"muscle_gain"|"endurance"|"strength"|"flexibility"|"maintenance")[]}'
        return schema, ["goals"]
    if stage == "final":
        schema = (
            '{"injuries": string[], "equipment": ("bodyweight"|"dumbbells"|"resistance_bands"|"gym_access")[], '
            '"preferred_workout_types": ("cardio"|"strength_training"|"yoga"|"pilates"|"HIIT")[], '
            '"preferred_training_times": ("morning"|"afternoon"|"evening")[], '
            '"not_preferred_exercises": string[], "special_considerations": string[]}'
        )
        return schema, []
    raise HTTPException(status_code=400, detail=f"Unsupported stage: {stage}")


def extract_fields_from_transcript(stage: str, transcript: str) -> Dict:
    """Use Groq LLM to extract structured fields from transcript for the given stage.

    Returns only the selections dictionary keyed to the current stage.
    """
    schema, _ = _schema_for_stage(stage)
    system = (
        "You extract structured fields from short spoken transcripts. Return ONLY minified JSON matching the schema. "
        "Normalize units: height in centimeters, weight in kilograms. If unknown, use null or an empty array. "
        "If the user says 'I am 5 feet 10 inches tall', convert to 177.8 cm."
    )
    user = f"Schema: {schema}\nTranscript: {transcript}"
    data = _call_groq_json(system, user)
    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Invalid extraction payload")
    return data


def compute_missing(stage: str, selections: Dict) -> List[str]:
    """Compute missing required fields per stage."""
    _, required = _schema_for_stage(stage)
    missing: List[str] = []
    for field in required:
        value = selections.get(field)
        if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
            missing.append(field)
    return missing


def save_upload_to_temp(upload) -> Path:
    """Persist an UploadFile-like object to a temporary file and return its path."""
    suffix = ""
    if hasattr(upload, "filename") and upload.filename:
        suffix = "." + upload.filename.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = upload.file.read()
        tmp.write(content)
        tmp.flush()
        return Path(tmp.name)


