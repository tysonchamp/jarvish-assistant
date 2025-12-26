import speech_recognition as sr
import os
import pygame
import time

class AudioManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()

    def listen(self):
        """
        Listens to the microphone and returns the recognized text.
        """
        with sr.Microphone() as source:
            print("Listening...")
            # self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Sorry, I could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None

    def play(self, file_path):
        """
        Plays an audio file.
        """
        if not file_path or not os.path.exists(file_path):
            print("Audio file not found.")
            return

        print(f"Playing: {file_path}")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
