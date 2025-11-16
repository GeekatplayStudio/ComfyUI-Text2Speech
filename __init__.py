import os
import json
import requests
import folder_paths

class HttpTTSToAudio:
    """
    Sends text to a local TTS server and returns an audio file path.
    Input: text (string), language (string), optional text_file_path
    Output: audio filepath (string)
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
                    "default": ""
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_path",)
    FUNCTION = "do_tts"
    CATEGORY = "Audio/TTS"

    def do_tts(self, text, language, server_url, text_file_path=""):
        if text_file_path:
            if os.path.isfile(text_file_path):
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
            else:
                raise RuntimeError(f"Text file not found: {text_file_path}")
        
        payload = {
            "text": text,
            "language": language
        }
        try:
            resp = requests.post(server_url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            path = data.get("path")
            if not path or not os.path.isfile(path):
                raise RuntimeError(f"No file returned from TTS server: {data}")
            # Copy to ComfyUI temp dir
            with open(path, "rb") as f:
                audio_bytes = f.read()
            temp_dir = folder_paths.get_temp_directory()
            out_name = os.path.basename(path)
            out_path = os.path.join(temp_dir, out_name)
            with open(out_path, "wb") as f:
                f.write(audio_bytes)
            return (out_path,)
        except Exception as e:
            print("TTS HTTP error:", e)
            return ("",)

class TTSServerStatus:
    """
    Checks if the TTS server is running.
    Input: server_url
    Output: status (string)
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
    CATEGORY = "Audio/TTS"

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