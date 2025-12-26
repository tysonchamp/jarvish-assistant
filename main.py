import sys
from config import WAKE_WORD
from audio_manager import AudioManager
from core import JarvisCore

def main():
    print("Initializing Jarvish Assistant...")
    
    jarvis = JarvisCore()
    audio = AudioManager()
    
    print(f"Comparison Wake Word: {WAKE_WORD}")
    print("Ready. Press Ctrl+C to exit.")

    try:
        while True:
            # 1. Listen for input
            user_text = audio.listen()
            
            if user_text:
                # For now, treat all input as a prompt since we are in a loop
                print(f"Processing: {user_text}")

                response_text, audio_file = jarvis.process_input(user_text)
                
                print(f"AI: {response_text}")

                # Play Audio
                if audio_file:
                    audio.play(audio_file)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
