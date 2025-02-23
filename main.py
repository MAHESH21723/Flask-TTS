from flask import Flask, render_template, request, jsonify, send_file
import pyttsx3
import os
import time
import glob

app = Flask(__name__)

# Ensure the output folder exists
OUTPUT_DIR = "static/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def cleanup_old_files():
    """ Remove old MP3 files to avoid storage overflow. """
    files = glob.glob(os.path.join(OUTPUT_DIR, "*.mp3"))
    if len(files) > 5:  # Keep only the latest 5 files
        for file in sorted(files)[:-5]:  
            os.remove(file)

def generate_audio(text, lang="en"):
    """ Generate speech audio from text and save it as an MP3 file. """
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speech speed
    engine.setProperty('volume', 1.0)  # Volume level

    voices = engine.getProperty('voices')

    # Set voice (Modify based on system support)
    if lang == "ta":  
        engine.setProperty('voice', voices[-1].id)  # Tamil (if available)
    else:
        engine.setProperty('voice', voices[0].id)  # Default English voice

    # Unique filename with timestamp to prevent caching
    filename = f"{int(time.time() * 1000)}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Generate and save speech
    engine.save_to_file(text, filepath)
    engine.runAndWait()

    cleanup_old_files()
    return f"/static/audio/{filename}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_audio', methods=['POST'])
def generate_audio_route():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        lang = data.get("lang", "en")

        if not text:
            return jsonify({"error": "Text input is empty!"}), 400

        audio_url = generate_audio(text, lang)
        return jsonify({"audio_url": audio_url + "?nocache=" + str(time.time())})  # Prevents browser caching

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_audio')
def download_audio():
    """ Download the latest generated audio file """
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.mp3")), reverse=True)
    if not files:
        return "No audio file found!", 404

    latest_file = files[0]
    return send_file(latest_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
