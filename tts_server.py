from flask import Flask, request, send_file, jsonify
import pyttsx3
import os
import uuid
from pydub import AudioSegment

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

    wav_name = f"{uuid.uuid4().hex}.wav"
    wav_path = os.path.join(OUTPUT_DIR, wav_name)
    mp3_name = f"{uuid.uuid4().hex}.mp3"
    mp3_path = os.path.join(OUTPUT_DIR, mp3_name)

    # Set properties if needed
    # engine.setProperty('voice', voice_id)  # for language, but pyttsx3 has limited support

    # Generate audio
    engine.save_to_file(text, wav_path)
    engine.runAndWait()

    # Convert to mp3
    try:
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format="mp3")
        os.remove(wav_path)  # remove wav
        return jsonify({
            "ok": True,
            "file": mp3_name,
            "path": mp3_path
        })
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

@app.route("/audio/<fname>", methods=["GET"])
def get_audio(fname):
    path = os.path.join(OUTPUT_DIR, fname)
    if not os.path.isfile(path):
        return jsonify({"error": "Not found"}), 404
    mimetype = "audio/mpeg" if fname.endswith(".mp3") else "audio/wav"
    return send_file(path, mimetype=mimetype)

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)