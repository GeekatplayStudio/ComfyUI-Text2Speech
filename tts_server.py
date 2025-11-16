from flask import Flask, request, send_file, jsonify
import pyttsx3
import os
import uuid

app = Flask(__name__)
engine = pyttsx3.init()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/tts", methods=["POST"])
def tts_route():
    data = request.get_json()
    text = data.get("text", "").strip()
    language = data.get("language", "en")  # pyttsx3 doesn't support language directly, but we can set voice

    if not text:
        return jsonify({"error": "No text"}), 400

    out_name = f"{uuid.uuid4().hex}.wav"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    # Set properties if needed
    # engine.setProperty('voice', voice_id)  # for language, but pyttsx3 has limited support

    # Generate audio
    engine.save_to_file(text, out_path)
    engine.runAndWait()

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