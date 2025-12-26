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

### prerequisites
- **Python 3.8+**
- **Ollama** running locally (`http://localhost:11434`)
- **Kokoro TTS API** running locally (`http://localhost:8880`)

### 1. Environment Setup (Miniconda)
Recommended for maintaining clean dependencies (tested on Ubuntu/Lubuntu 24).

```bash
# 1. Create a new environment
conda create -n jarvish python=3.10
conda activate jarvish

# 2. Install Audio & System Dependencies
# Note: Lubuntu/Ubuntu might require these for PyAudio and Screenshot tools
sudo apt-get update
sudo apt-get install ffmpeg scrot

# 3. Install Python Packages
pip install -r requirements.txt
```

### 2. Database Setup (MySQL)
    *   Ensure you have a MySQL server running (e.g., via XAMPP, Docker, or local install).
    *   Create a database (default name: `jarvish_db`) or let the setup script do it for you.
    *   Initialize the database tables:
        ```bash
        python setup_db.py
        ```
    *   (Optional) Update `config.py` or set environment variables `DB_HOST`, `DB_USER`, `DB_PASSWORD` if your MySQL configuration differs from default.

4. **Configuration (Optional)**:
   You can modify `config.py` to change models (e.g., `gemma3:latest`), voices, or database credentials.

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
   **Autoplay Note**: Mobile browsers often require one user interaction (tap anywhere) before allowing auto-playing audio. If audio doesn't play automatically, try interacting with the page first.

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
