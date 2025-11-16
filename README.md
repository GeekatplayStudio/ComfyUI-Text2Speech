# ComfyUI TTS HTTP Custom Node

This custom node allows ComfyUI to integrate with a local TTS server for generating audio from text.

## Setup

### 1. Install TTS Server

Run `install.bat` to set up the virtual environment and install dependencies.

### 2. Run TTS Server

Run `run_tts.bat` to start the TTS server on `http://127.0.0.1:5002`.

### 3. Install Dependencies in ComfyUI

Ensure `requests` is installed in your ComfyUI environment:

```bash
pip install requests
```

### 4. Restart ComfyUI

Restart ComfyUI to load the custom node. You should see `HttpTTSToAudio` under `Audio/TTS`.

## Usage

- Input text and language.
- The node sends a POST request to the TTS server.
- Returns the path to the generated audio file.

## Workflow Example

Connect the output `audio_path` to audio loading nodes in your ComfyUI workflow for video/audio processing.