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
    /* Premium Chat Styling */
    .stChatMessage {
        background-color: #1e2126;
        border: 1px solid #2e3035;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
    /* Floating Mic Button */
    div.element-container:has(div#mic-container) + div.element-container {
        position: fixed;
        bottom: 22px;
        right: 15px; /* Right side like WhatsApp */
        z-index: 999999;
        width: auto;
    }
    
    /* Adjust Chat Input to make space for Mic */
    div[data-testid="stChatInput"] {
        padding-right: 10px !important;
    }
    
    /* Input Fields Styling */
    textarea[data-testid="stChatInputTextArea"] {
        background-color: #1e2126;
        color: white;
        border-radius: 20px;
    }
    
    /* Scroll padding */
    .main .block-container {
        padding-bottom: 150px;
    }
    
</style>
""", unsafe_allow_html=True)

st.title("🤖 Jarvish Assistant")
# Hide the hint to look cleaner
# st.markdown("I am your AI companion. Enable **Mobile/Browser** output for auto-play response.")

# Sidebar for options
with st.sidebar:
    st.header("Settings")
    
    # Mode Selector
    interaction_mode = st.radio("Interface Mode", ["Text Chat 💬", "Voice Chat 🎙️"], index=0)
    st.write("---")
    
    st.write("Voice: af_heart (Kokoro)")
    # dynamically get models from config.py
    st.write("Model: " + OLLAMA_MODEL + " (Ollama)")
    
    output_mode = st.radio("Audio Output", ["Desktop Speakers", "Mobile/Browser", "Both"], index=0)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display Chat History with Avatars
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"])

prompt = None
audio_bytes = None

# Voice Mode Interface
if "Voice" in interaction_mode:
    # Mic Recorder (Floating)
    st.markdown('<div id="mic-container"></div>', unsafe_allow_html=True)
    from streamlit_mic_recorder import mic_recorder
    audio_capture = mic_recorder(
        start_prompt="🎙️",
        stop_prompt="⏹️", 
        key="recorder",
        just_once=True,
        use_container_width=False
    )
    if audio_capture:
        audio_bytes = audio_capture['bytes']

# Text Mode Interface
if "Text" in interaction_mode:
    # Chat Input (Native Sticky)
    user_input = st.chat_input("Type your message...")
    if user_input:
        prompt = user_input

# Logic to prioritize inputs
if prompt:
    # prompt is already set from Text Mode or Voice Mode above if applicable
    pass
elif audio_bytes:
    # If no text prompt, check for audio bytes from Voice Mode
    # audio_bytes is set above if applicable
    st.toast("Processing audio...")
    
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
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Thinking State
    with st.chat_message("assistant", avatar="🤖"):
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
                # autoplay=True requires Streamlit 1.33+
                st.audio(audio_file, format="audio/mp3", autoplay=True)
    
    # Add Assistant Message to History
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_text,
        "audio": audio_file if output_mode in ["Mobile/Browser", "Both"] else None
    })
