# ComfyUI-Text2Speech

A ComfyUI custom node for text-to-speech integration with a local TTS server.

## Features

- Custom ComfyUI node `HttpTTSToAudio` for sending text to a local TTS server.
- Local TTS server using Coqui TTS (XTTS v2 model).
- Easy setup with batch files for Windows.

## Installation

### TTS Server Setup

1. Run `install.bat` to create a virtual environment and install dependencies.
2. Run `run_tts.bat` to start the TTS server on `http://127.0.0.1:5002`.

### ComfyUI Node

1. Copy the `__init__.py` file to your ComfyUI `custom_nodes` folder (e.g., `ComfyUI/custom_nodes/ComfyUI_Text2Speech/__init__.py`).
2. Install `requests` in your ComfyUI environment: `pip install requests`.
3. Restart ComfyUI.

## Usage

- Use the `HttpTTSToAudio` node in ComfyUI under `Audio/TTS`.
- Input text, language, and server URL.
- Output is the path to the generated audio file.

## Workflow

Connect the audio path to audio/video processing nodes in ComfyUI for creating TTS-enhanced content.