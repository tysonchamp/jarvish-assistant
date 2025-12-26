# 🤖 Jarvish Assistant

**Jarvish** is a modular, voice-activated AI assistant integrated with local LLMs (Ollama) and high-quality Text-to-Speech (Kokoro). It features both a command-line interface and a modern web dashboard.

![Jarvis](https://img.shields.io/badge/AI-Ollama-blue) ![TTS](https://img.shields.io/badge/TTS-Kokoro-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

## ✨ Features

- **🗣️ Voice Interaction**: Seamless Speech-to-Text and Text-to-Speech loop.
- **🧠 Local Intelligence**: Powered by **Ollama** (Llama 3, Mistral, etc.).
- **👁️ Vision & Screen Reading**:
  - Analyze images.
  - **"Read my screen"**: Takes a screenshot of your active monitor and analyzes it.
- **🔊 Natural Voice**: Uses **Kokoro TTS** for realistic speech synthesis.
- **💻 Dual Interface**:
  - **CLI**: Terminal-based lightweight interaction.
  - **Web UI**: Streamlit-based dashboard with chat history and voice input (mobile compatible).

## 🚀 Installation

### Prerequisites
- **Python 3.8+**
- **Ollama** running locally (`http://localhost:11434`)
- **Kokoro TTS API** running locally (`http://localhost:8880`)

### 1. System Dependencies (Linux)
```bash
# Audio drivers
sudo apt-get install python3-pyaudio portaudio19-dev ffmpeg

# Screenshot tools
sudo apt-get install scrot python3-tk python3-dev
```

### 2. Install Python Packages
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Option A: Web UI (Mobile Input / Desktop Output)
1. Run `streamlit run app.py` on your desktop.
2. Note the **Network URL** (e.g., `http://192.168.1.5:8501`) displayed in the terminal.
3. Open this URL on your mobile browser.
4. Use the sidebar to set **Audio Output** to "Desktop Speakers".
5. Speak into your mobile device. **Jarvish** will execute the task on your desktop (e.g., read screen) and reply through your **desktop speakers**.

### Option B: Command Line
The classic terminal experience.
```bash
python3 main.py
```
- Speaks out loud using system speakers.
- Listens via default microphone.

### Troubleshooting Mobile Audio
Modern browsers block microphone access on "insecure" origins (HTTP remote IP). To fix this:
1. **Option A (Recommended)**: Use [ngrok](https://ngrok.com/) to tunnel your localhost to an HTTPS URL.
   ```bash
   ngrok http 8501
   ```
2. **Option B (Chrome Flags)**:
   - Go to `chrome://flags/#unsafely-treat-insecure-origin-as-secure` on your mobile browser.
   - Add your computer's IP (e.g., `http://192.168.1.5:8501`).
   - Enable and restart chrome.

## ⚙️ Configuration

Edit `config.py` or set environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API URL |
| `OLLAMA_MODEL` | `llama3` | Text Model |
| `IMAGE_MODEL` | `gemma` | Vision Model |
| `TTS_ENDPOINT` | `.../v1/audio/speech` | Kokoro TTS Endpoint |
| `WAKE_WORD` | `jarvis` | Activation word (CLI) |

## 📁 Project Structure

- `core.py`: Central logic for LLM/TTS/Audio orchestration.
- `app.py`: Streamlit Web Application.
- `main.py`: CLI Entry point.
- `ollama_client.py`: Ollama API wrapper.
- `tts_client.py`: Kokoro TTS wrapper.
- `audio_manager.py`: Audio I/O utilities.
- `utils.py`: System utilities (Screen capture).
