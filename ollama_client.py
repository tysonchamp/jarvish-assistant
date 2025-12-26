import requests
import json
import base64
from config import OLLAMA_HOST, OLLAMA_MODEL, IMAGE_MODEL

class OllamaClient:
    def __init__(self, host=OLLAMA_HOST, model=OLLAMA_MODEL, vision_model=IMAGE_MODEL):
        self.host = host
        self.model = model
        self.vision_model = vision_model
        self.chat_history = []

    def chat(self, user_input, image_path=None):
        """
        Sends a message to Ollama. If image_path is provided, uses the vision model.
        """
        messages = self.chat_history + [{"role": "user", "content": user_input}]
        
        payload = {
            "model": self.vision_model if image_path else self.model,
            "messages": messages,
            "stream": False
        }

        if image_path:
            try:
                with open(image_path, "rb") as img_file:
                    b64_image = base64.b64encode(img_file.read()).decode('utf-8')
                    # OpenAI/Ollama compatible vision request often expects images in the message
                    # But for standard Ollama /api/chat, it's 'images': [b64]
                    # Let's check if we are using the official python client or raw requests. 
                    # Using raw requests to /api/chat.
                    payload['messages'][-1]['images'] = [b64_image]
            except Exception as e:
                print(f"Error loading image: {e}")
                return "I couldn't read the image."

        try:
            response = requests.post(f"{self.host}/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            
            assistant_message = result.get("message", {}).get("content", "")
            
            # Update history (append both user and assistant message)
            # Note: For vision requests, we might not want to keep the heavy base64 image in history for every turn 
            # if the context window is small, but for now we'll clean it up or keep standard text history.
            
            # Store history without the image data to save space if it was a vision request
            if image_path:
                 # Remove image from the last user message in history before saving
                 payload['messages'][-1].pop('images')
            
            self.chat_history.append({"role": "user", "content": user_input})
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message

        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {e}"
