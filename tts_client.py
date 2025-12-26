import requests
import os
from config import TTS_ENDPOINT, TTS_VOICE, TTS_SPEED

class KokoroClient:
    def __init__(self, endpoint=TTS_ENDPOINT, voice=TTS_VOICE, speed=TTS_SPEED):
        self.endpoint = endpoint
        self.voice = voice
        self.speed = speed

    def generate_audio(self, text, output_file="output.mp3"):
        """
        Generates audio from text using Kokoro TTS and saves it to a file.
        Returns the path to the saved file or None if failed.
        """
        payload = {
            "model": "kokoro",
            "input": text,
            "voice": self.voice,
            "response_format": "mp3",
            "speed": self.speed
        }
        
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
