import speech_recognition as sr
import os
import pygame
import time

class AudioManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # pygame.mixer.init() # Lazy load in play()

    def listen(self, timeout=5, phrase_time_limit=10):
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            if p.get_device_count() == 0:
                print("AudioManager: No audio input devices found. Skipping listen.")
                p.terminate()
                return None
            p.terminate()
        except Exception as e:
            print(f"AudioManager: Error checking audio devices: {e}")
            pass

        try:
            with sr.Microphone() as source:
                # print("Listening...") # Reduced verbosity
                # self.recognizer.adjust_for_ambient_noise(source) # Optional: dynamic adjustment
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    text = self.recognizer.recognize_google(audio)
                    print(f"User (Mic): {text}")
                    return text
                except sr.WaitTimeoutError:
                    return None
                except sr.UnknownValueError:
                    # print("Sorry, I could not understand audio.") # Reduced verbosity
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None
        except (AttributeError, OSError) as e:
            print(f"microphone error: {e}")
            return None

    def play(self, file_path):
        """
        Plays an audio file.
        """
        if not file_path or not os.path.exists(file_path):
            print("Audio file not found.")
            return

        print(f"Playing: {file_path}")
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
