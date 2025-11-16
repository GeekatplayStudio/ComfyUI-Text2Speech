from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import os
import uuid

# Choose a model (example: XTTS v2 multilingual; you can pick any supported model)
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

app = Flask(__name__)
tts = TTS(MODEL_NAME)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/tts", methods=["POST"])
def tts_route():
    data = request.get_json()
    text = data.get("text", "").strip()
    speaker = data.get("speaker")  # optional
    language = data.get("language", "en")  # optional

    if not text:
        return jsonify({"error": "No text"}), 400

    out_name = f"{uuid.uuid4().hex}.wav"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    # Generate audio
    # For XTTS you can pass language, speaker_wav, etc.; adjust to your chosen model
    tts.tts_to_file(
        text=text,
        file_path=out_path,
        language=language
    )

    return jsonify({
        "ok": True,
        "file": out_name,
        "path": out_path
    })

@app.route("/audio/<fname>", methods=["GET"])
def get_audio(fname):
    path = os.path.join(OUTPUT_DIR, fname)
    if not os.path.isfile(path):
        return jsonify({"error": "Not found"}), 404
    return send_file(path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)