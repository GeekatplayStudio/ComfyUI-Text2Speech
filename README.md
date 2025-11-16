# ComfyUI Text-to-Speech Node

**GeekatPlay Studio** - https://github.com/GeekatPlayStudio

High-quality text-to-speech integration for ComfyUI workflows using Microsoft Edge TTS.

## Features

- **High-Quality Neural Voices**: Powered by Microsoft Edge TTS with natural-sounding voices
- **13 Voice Options**: Multiple English variants (US, GB, AU, CA, IN) with male and female voices
- **Flexible Input**: Direct text input or load from text file
- **Customizable Output**: Choose output directory or use ComfyUI default
- **Adjustable Parameters**: Control speech rate (50-400) and volume (0.0-1.0)
- **Server Health Check**: Built-in status node to verify server connectivity
- **Fallback Support**: Automatic fallback to pyttsx3 if Edge TTS is unavailable

## Installation

1. Clone or copy this folder to your ComfyUI custom_nodes directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the TTS server:
   ```bash
   python tts_server.py
   ```
   The server will run on `http://127.0.0.1:5002`

## Usage

### Nodes

**HttpTTSToAudio** (Category: `geekatplay/TTS`)
- Converts text to speech audio file
- Required inputs:
  - `text`: Text to convert to speech (multiline)
  - `language`: Language code (default: "en")
  - `server_url`: TTS server endpoint (default: http://127.0.0.1:5002/tts)
- Optional inputs:
  - `text_file_path`: Load text from file (file picker)
  - `output_directory`: Save location (directory picker)
  - `voice`: Voice selection dropdown (13 Edge TTS voices)
  - `rate`: Speech rate 50-400 (default: 180)
  - `volume`: Volume 0.0-1.0 (default: 1.0)
- Output: `audio_path` (STRING) - Path to generated WAV file

**TTSServerStatus** (Category: `geekatplay/TTS`)
- Checks if TTS server is running
- Input: `server_url` (default: http://127.0.0.1:5002/status)
- Output: `status` (STRING) - Server status message

### Available Voices

- **US English**: AriaNeural (F), ZiraNeural (F), JennyNeural (F), GuyNeural (M)
- **British English**: SoniaNeural (F), RyanNeural (M), LibbyNeural (F)
- **Australian English**: NatashaNeural (F), WilliamNeural (M)
- **Canadian English**: ClaraNeural (F), LiamNeural (M)
- **Indian English**: NeerjaNeural (F), PrabhatNeural (M)

## Workflow Example

1. Add `TTSServerStatus` node to verify server is running
2. Add `HttpTTSToAudio` node
3. Configure text, voice, and parameters
4. Connect output to audio processing nodes (e.g., VHS_LoadAudio, WAS_SaveAudio)

## Technical Details

- **Primary Engine**: Microsoft Edge TTS (requires internet for high-quality neural voices)
- **Fallback Engine**: pyttsx3 (offline, uses system voices)
- **Output Format**: WAV audio files
- **Server**: Flask on localhost:5002

## Troubleshooting

**Server not running:**
- Start the server: `python tts_server.py`
- Verify port 5002 is not in use

**No audio generated:**
- Check internet connection (Edge TTS requires online access)
- Review server console for error messages
- Verify output directory write permissions

**Voice not working:**
- Edge TTS voices require internet connection
- Offline mode uses pyttsx3 fallback with system voices
- Ensure voice name matches dropdown options

## Requirements

- Python 3.8+
- Internet connection (for Edge TTS)
- Dependencies: edge-tts, pyttsx3, flask, requests

## License

GeekatPlay Studio

