import requests
import os
from config import TTS_ENDPOINT, TTS_VOICE, TTS_SPEED

class KokoroClient:
    def __init__(self, endpoint=TTS_ENDPOINT, voice=TTS_VOICE, speed=TTS_SPEED):
        self.endpoint = endpoint
        self.voice = voice
        self.speed = speed

    def generate_audio(self, text, output_file=None):
        """
        Generates audio from text using Kokoro TTS and saves it to a unique file.
        Returns the path to the saved file or None if failed.
        """
        payload = {
            "model": "kokoro",
            "input": text,
            "voice": self.voice,
            "response_format": "mp3",
            "speed": self.speed
        }
        
        # Determine output path
        if output_file is None:
            from config import AUDIO_STORAGE_PATH
            import time
            import uuid
            
            # Ensure directory exists
            if not os.path.exists(AUDIO_STORAGE_PATH):
                os.makedirs(AUDIO_STORAGE_PATH)
                
            # Create unique filename: audio_<timestamp>_<short_uuid>.mp3
            timestamp = int(time.time())
            unique_id = str(uuid.uuid4())[:8]
            filename = f"audio_{timestamp}_{unique_id}.mp3"
            output_file = os.path.join(AUDIO_STORAGE_PATH, filename)
        
        try:
            response = requests.post(self.endpoint, json=payload, stream=True)
            response.raise_for_status()
            
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return output_file
        except requests.exceptions.RequestException as e:
            print(f"Error generating audio: {e}")
            return None
