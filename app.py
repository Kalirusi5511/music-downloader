from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Keine URL angegeben"}), 400

    file_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        expected_file = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp3")
        if os.path.exists(expected_file):
            return jsonify({
                "success": True,
                "file": expected_file,
                "download_url": f"/file/{file_id}.mp3"
            })
        else:
            return jsonify({"error": "Datei wurde nicht gefunden"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/file/<filename>")
def serve_file(filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "Datei nicht gefunden"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
