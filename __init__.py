import os
import json
import requests
import folder_paths

class HttpTTSToAudio:
    """
    Sends text to a local TTS server and returns an audio file path.
    Input: text (string), language (string)
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
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_path",)
    FUNCTION = "do_tts"
    CATEGORY = "Audio/TTS"

    def do_tts(self, text, language, server_url):
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

NODE_CLASS_MAPPINGS = {
    "HttpTTSToAudio": HttpTTSToAudio,
}