import streamlit as st
import time
from core import JarvisCore
from audio_manager import AudioManager
from config import OLLAMA_MODEL
import os

# Page Config
st.set_page_config(page_title="Jarvish Assistant", page_icon="🤖", layout="centered")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "jarvis" not in st.session_state:
    st.session_state.jarvis = JarvisCore()
if "audio_manager" not in st.session_state:
    st.session_state.audio_manager = AudioManager()

# Custom CSS for "premium" feel
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
    }
    /* Animated Thinking */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .thinking {
        animation: pulse 1.5s infinite;
        color: #4facfe;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Jarvish Assistant")
st.markdown("I am your AI companion. Speak or type to interact.")

# Sidebar for options
with st.sidebar:
    st.header("Settings")
    st.write("Voice: af_heart (Kokoro)")
    # dynamically get models from config.py
    st.write("Model: " + OLLAMA_MODEL + " (Ollama)")
    
    output_mode = st.radio("Audio Output", ["Desktop Speakers", "Mobile/Browser", "Both"], index=0)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"])

# Input Handling
user_input = st.chat_input("Type your message here...")

# Audio Input (Standard JS Recorder)
from streamlit_mic_recorder import mic_recorder

st.info("💡 Note: Microphone access on mobile requires **HTTPS** or **localhost**. If using HTTP over WiFi, refer to the README for browser configuration.")

# Capture audio
# keys are important to prevent reloading issues
audio_capture = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="recorder"
)

# Process Input
prompt = None
if user_input:
    prompt = user_input
elif audio_capture:
    st.toast("Audio captured! Processing...")
    
    # audio_capture is a dict: {'bytes': b'...', 'sample_rate': ...}
    audio_bytes = audio_capture['bytes']
    
    # Use pydub to convert to compatible WAV
    from pydub import AudioSegment
    import io
    
    try:
        # Load the audio bytes
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Export to a clean WAV format that SpeechRecognition likes (PCM)
        buffer = io.BytesIO()
        audio_segment.export(buffer, format="wav")
        buffer.seek(0)
        
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(buffer) as source:
            # record the audio from the file
            audio_data = r.record(source)
            try:
                prompt = r.recognize_google(audio_data)
                st.toast(f"Recognized: {prompt}")
            except sr.UnknownValueError:
                st.error("Could not understand audio.")
            except sr.RequestError as e:
                st.error(f"Could not request results; {e}")
                
    except Exception as e:
        st.error(f"Error processing audio: {e}")

if prompt:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Thinking State
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown('<span class="thinking">Thinking...</span>', unsafe_allow_html=True)
        
        # Process via Core
        # Note: 'read my screen' in web context might grab server screen, which is usually not what user wants on mobile.
        # But we will keep logic consistent.
        response_text, audio_file = st.session_state.jarvis.process_input(prompt)
        
        # Display Response
        message_placeholder.markdown(response_text)
        
        if audio_file:
            # Play on Desktop (Server)
            if output_mode in ["Desktop Speakers", "Both"]:
                st.toast("Playing audio on Desktop...")
                st.session_state.audio_manager.play(audio_file)
            
            # Play on Mobile (Browser)
            if output_mode in ["Mobile/Browser", "Both"]:
                st.audio(audio_file)
    
    # Add Assistant Message to History
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_text,
        "audio": audio_file if output_mode in ["Mobile/Browser", "Both"] else None
    })
