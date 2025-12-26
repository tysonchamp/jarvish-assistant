import os

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:latest") # Default text model
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gemma3:latest") # Vision model

# Kokoro TTS Configuration
# Based on the openapi-kokorotts.json, the speech endpoint is /v1/audio/speech
TTS_BASE_URL = os.getenv("TTS_BASE_URL", "http://localhost:8880")
TTS_ENDPOINT = f"{TTS_BASE_URL}/v1/audio/speech"
TTS_VOICE = os.getenv("TTS_VOICE", "af_heart")
TTS_SPEED = float(os.getenv("TTS_SPEED", "1.0"))

# Audio Configuration
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis")

# Utils Configuration
SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "/tmp/screenshot.png")
