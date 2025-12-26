from ollama_client import OllamaClient
from tts_client import KokoroClient
from utils import take_screenshot
import os

class JarvisCore:
    def __init__(self):
        self.ollama = OllamaClient()
        self.tts = KokoroClient()
    
    def process_input(self, user_text, image_path=None):
        """
        Processes user text input, handles 'read my screen' logic if not already provided,
        queries Ollama, and returns the response text and generated audio path.
        """
        if not user_text:
            return None, None

        # Check for screen reading trigger if image not already provided
        if not image_path and ("read my screen" in user_text.lower() or "look at my screen" in user_text.lower()):
            print(" Taking screenshot...")
            image_path = take_screenshot()
        
        # Get Response from LLM
        response_text = self.ollama.chat(user_text, image_path=image_path)
        
        # Generate Audio
        # We use a temporary filename or a unique one to avoid conflicts in web usage?
        # For now, tts_client uses a default "output.mp3".
        # Let's make it return unique files or handle it in the client if needed.
        # For now, we will stick to the simple client behavior but maybe use a timestamped file in app.py.
        # But here, let's just call generate.
        audio_file = self.tts.generate_audio(response_text)
        
        return response_text, audio_file
