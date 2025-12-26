import streamlit as st
import time
from core import JarvisCore
from audio_manager import AudioManager
from config import OLLAMA_MODEL, OLLAMA_HOST, EMBADDING_MODEL
import os

# Page Config
st.set_page_config(page_title="Jarvish Assistant", page_icon="🤖", layout="centered")

from db_manager import DBManager

if "db" not in st.session_state:
    st.session_state.db = DBManager()
    st.session_state.db.create_tables() # Ensure tables exist on startup

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

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
    st.header("🗂️ History")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_conversation_id = None
        st.session_state.messages = []
        st.rerun()
        
    # Load Conversations
    conversations = st.session_state.db.get_conversations()
    if conversations:
        st.write("---")
        for conv in conversations:
            # Highlight current chat
            button_style = "primary" if st.session_state.current_conversation_id == conv['id'] else "secondary"
            if st.button(f"💬 {conv['title']}", key=f"conv_{conv['id']}", use_container_width=True, type=button_style):
                st.session_state.current_conversation_id = conv['id']
                # Load messages for this conversation
                db_messages = st.session_state.db.get_messages(conv['id'])
                # Convert DB messages to Session State format
                st.session_state.messages = []
                for msg in db_messages:
                    st.session_state.messages.append({
                        "role": msg['role'],
                        "content": msg['content'],
                        "audio": msg['audio_path']  # Assuming we store path or None
                    })
                st.rerun()

    st.write("---")
    st.header("Settings")
    
    # Mode Selector
    interaction_mode = st.radio("Interface Mode", ["Text Chat 💬", "Voice Chat 🎙️"], index=0)
    st.write("---")
    
    st.write("Voice: af_heart (Kokoro)")
    # dynamically get models from config.py
    st.write("Model: " + OLLAMA_MODEL + " (Ollama)")
    
    output_mode = st.radio("Audio Output", ["Desktop Speakers", "Mobile/Browser", "Both"], index=0)
    
    if st.button("Clear Chat"):
        # Helper to clear current chat messages from memory (not DB)
        st.session_state.messages = []
        if st.session_state.current_conversation_id:
             st.session_state.db.delete_conversation(st.session_state.current_conversation_id)
             st.session_state.current_conversation_id = None
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
    # Handle New Conversation Creation
    if st.session_state.current_conversation_id is None:
        # Create new conversation in DB
        # Initial title is the prompt (truncated) or "New Chat"
        initial_title = (prompt[:30] + '...') if len(prompt) > 30 else prompt
        new_id = st.session_state.db.create_conversation(title=initial_title)
        st.session_state.current_conversation_id = new_id
        
        # Trigger Title Generation in Background (Simulated)
        # We can update the title properly using LLM
        try:
           # Simple direct title generation call
           from ollama_client import OllamaClient
           client = OllamaClient(model=EMBADDING_MODEL) # Use specified model for titling
           # Short non-conversational request
           title_prompt = f"Generate a short, concise (3-5 words) chat title for this opening message: '{prompt}'. Do not include quotes."
           
           # Let's do a direct request for title to avoid messing up main chat history context
           import requests
           import json
           from config import OLLAMA_HOST
           
           title_payload = {
               "model": EMBADDING_MODEL,
               "prompt": title_prompt,
               "stream": False
           }
           res = requests.post(f"{OLLAMA_HOST}/api/generate", json=title_payload)
           if res.status_code == 200:
               final_title = res.json().get("response", "").strip().strip('"')
               # Update DB
               conn = st.session_state.db.get_connection()
               cursor = conn.cursor()
               cursor.execute("UPDATE conversations SET title = %s WHERE id = %s", (final_title, new_id))
               conn.commit()
               cursor.close()
               conn.close()
               st.rerun() # Refresh sidebar to show new title
        except Exception as e:
            print(f"Title generation failed: {e}")

    # Add User Message to State and DB
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.db.add_message(st.session_state.current_conversation_id, "user", prompt)
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Thinking State
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown('<span class="thinking">Thinking...</span>', unsafe_allow_html=True)
        
        # Process via Core
        response_text, audio_file = st.session_state.jarvis.process_input(prompt)
        
        # Display Response
        message_placeholder.markdown(response_text)
        
        # Add Assistant Message to History and DB (BEFORE Playback)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_text,
            "audio": audio_file if output_mode in ["Mobile/Browser", "Both"] else None
        })
        st.session_state.db.add_message(
            st.session_state.current_conversation_id, 
            "assistant", 
            response_text, 
            audio_path=audio_file if output_mode in ["Mobile/Browser", "Both"] else None
        )
        
        if audio_file:
            # Play on Desktop (Server)
            if output_mode in ["Desktop Speakers", "Both"]:
                st.toast("Playing audio on Desktop...")
                st.session_state.audio_manager.play(audio_file)
            
            # Play on Mobile (Browser)
            if output_mode in ["Mobile/Browser", "Both"]:
                # autoplay=True requires Streamlit 1.33+
                st.audio(audio_file, format="audio/mp3", autoplay=True)


