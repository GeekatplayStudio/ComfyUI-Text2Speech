""" 
TTS Server for ComfyUI Text-to-Speech Node
GeekatPlay Studio

GitHub: https://github.com/GeekatPlayStudio
YouTube: @geekatplay | @geekatplay-ru (Russian)
Patreon: https://patreon.com/geekatplay

Flask server providing text-to-speech via Microsoft Edge TTS with pyttsx3 fallback.
Runs on localhost:5002

Endpoints:
- POST /tts: Generate speech audio from text
- GET /status: Server health check
"""

from flask import Flask, request, jsonify
import os
import uuid
import asyncio
import pyttsx3

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/tts", methods=["POST"])
def tts_route():
    """Generate speech audio from text using Edge TTS or pyttsx3 fallback."""
    data = request.get_json()
    text = data.get("text", "").strip()
    voice = data.get("voice", "en-US-AriaNeural").strip()
    rate = data.get("rate", 180)
    volume = data.get("volume", 1.0)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Generate unique filename
    wav_name = f"{uuid.uuid4().hex}.wav"
    wav_path = os.path.abspath(os.path.join(OUTPUT_DIR, wav_name))
    
    # Try Edge TTS first (high-quality neural voices)
    try:
        from edge_tts import Communicate
        communicate = Communicate(text, voice)
        asyncio.run(communicate.save(wav_path))
        
        if os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
            return jsonify({
                "ok": True,
                "file": wav_name,
                "path": wav_path
            })
        else:
            return jsonify({"error": "Failed to generate audio"}), 500
            
    except Exception as e:
        # Fallback to pyttsx3 if Edge TTS fails
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            
            # Save speech to file
            engine.save_to_file(text, wav_path)
            engine.runAndWait()
            
            # Return success response
            if os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
                return jsonify({
                    "ok": True,
                    "file": wav_name,
                    "path": wav_path
                })
            else:
                return jsonify({"error": "Failed to generate audio"}), 500
                
        except Exception as e2:
            return jsonify({"error": f"TTS failed: {str(e2)}"}), 500

@app.route("/status", methods=["GET"])
def status():
    """Health check endpoint to verify server is running."""
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)