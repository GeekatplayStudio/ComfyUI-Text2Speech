""" 
ComfyUI Text-to-Speech Node
GeekatPlay Studio

GitHub: https://github.com/GeekatPlayStudio
YouTube: @geekatplay | @geekatplay-ru (Russian)
Patreon: https://patreon.com/geekatplay

Provides high-quality text-to-speech using Microsoft Edge TTS with pyttsx3 fallback.
Requires a local Flask server (tts_server.py) running on port 5002.
"""

import os
import requests
import folder_paths

class HttpTTSToAudio:
    """
    Text-to-Speech node that connects to a local TTS server.
    
    Features:
    - High-quality neural voices via Microsoft Edge TTS
    - 13 voice options across US, GB, AU, CA, and IN English variants
    - Text file input support
    - Custom output directory selection
    - Adjustable speech rate and volume
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello from ComfyUI."
                }),
                "language": ("STRING", {
                    "default": "en"
                }),
                "server_url": ("STRING", {
                    "default": "http://127.0.0.1:5002/tts"
                })
            },
            "optional": {
                "text_file_path": ("STRING", {
                    "default": "",
                    "file_picker": "file"
                }),
                "output_directory": ("STRING", {
                    "default": "",
                    "file_picker": "directory"
                }),
                "voice": ([
                    "en-US-AriaNeural", 
                    "en-US-ZiraNeural", 
                    "en-US-JennyNeural", 
                    "en-US-GuyNeural",
                    "en-GB-SoniaNeural", 
                    "en-GB-RyanNeural", 
                    "en-GB-LibbyNeural",
                    "en-AU-NatashaNeural", 
                    "en-AU-WilliamNeural",
                    "en-CA-ClaraNeural", 
                    "en-CA-LiamNeural",
                    "en-IN-NeerjaNeural", 
                    "en-IN-PrabhatNeural"
                ],),
                "rate": ("INT", {
                    "default": 180,
                    "min": 50,
                    "max": 400
                }),
                "volume": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0
                })
                ,
                "timeout_seconds": ("INT", {
                    "default": 300,
                    "min": 60,
                    "max": 3600,
                    "step": 10
                })
                ,
                "auto_timeout": ("BOOLEAN", {
                    "default": True
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_path",)
    FUNCTION = "do_tts"
    CATEGORY = "geekatplay/TTS"

    def do_tts(self, text, language, server_url, text_file_path="", output_directory="", voice="en-US-AriaNeural", rate=180, volume=1.0, timeout_seconds=300, auto_timeout=True):
        # Load text from file if provided
        source_filename = "tts_output"
        if text_file_path:
            if os.path.isfile(text_file_path):
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                # Extract filename without extension for output naming
                source_filename = os.path.splitext(os.path.basename(text_file_path))[0]
            else:
                raise RuntimeError(f"Text file not found: {text_file_path}")
        
        # Prepare request payload for TTS server
        payload = {
            "text": text,
            "language": language,
            "voice": voice,
            "rate": rate,
            "volume": volume
        }
        
        try:
            # Determine effective timeout
            if auto_timeout:
                words = len(text.split())
                estimated_seconds = int(((words / 2.5) * 1.3) + 10)  # words/sec ~2.5; add 30% buffer + setup
                estimated_seconds = max(60, min(3600, estimated_seconds))
                effective_timeout = max(timeout_seconds, estimated_seconds)
            else:
                effective_timeout = timeout_seconds

            # Send TTS request to local server
            resp = requests.post(server_url, json=payload, timeout=effective_timeout)
            resp.raise_for_status()
            data = resp.json()
            
            path = data.get("path")
            if not path or not os.path.isfile(path):
                raise RuntimeError(f"No file returned from TTS server: {data}")
            
            # Copy audio file to output directory
            with open(path, "rb") as f:
                audio_bytes = f.read()
            
            # Determine output directory
            out_dir = output_directory.strip() if output_directory.strip() else folder_paths.get_output_directory()
            os.makedirs(out_dir, exist_ok=True)
            
            # Generate descriptive filename: originalname_voice_YYYYMMDD_HHMMSS.wav
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            voice_short = voice.replace("en-", "").replace("-Neural", "")  # e.g., "US-Aria"
            out_name = f"{source_filename}_{voice_short}_{timestamp}.wav"
            out_path = os.path.join(out_dir, out_name)
            with open(out_path, "wb") as f:
                f.write(audio_bytes)
            
            return (out_path,)
        except Exception as e:
            raise RuntimeError(f"TTS request failed: {str(e)}")

class TTSServerStatus:
    """
    Health check node for the TTS server.
    Verifies that the Flask TTS server is running and accessible.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "server_url": ("STRING", {
                    "default": "http://127.0.0.1:5002/status"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "check_status"
    CATEGORY = "geekatplay/TTS"

    def check_status(self, server_url):
        try:
            resp = requests.get(server_url, timeout=5)
            if resp.status_code == 200:
                return ("Server is running",)
            else:
                return (f"Server responded with status {resp.status_code}",)
        except requests.exceptions.RequestException as e:
            return (f"Server not running or unreachable: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "HttpTTSToAudio": HttpTTSToAudio,
    "TTSServerStatus": TTSServerStatus,
}