from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Home
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        for f in info['formats']:
            if f.get('height'):
                formats.append({
                    'format_id': f['format_id'],
                    'quality': f"{f['height']}p",
                    'ext': f['ext']
                })

        return render_template("index.html", video=info, formats=formats)

    return render_template("index.html")

# Download Route
@app.route("/download")
def download():
    url = request.args.get("url")
    format_id = request.args.get("format_id")

    ydl_opts = {
        'format': format_id,
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return send_file(filename, as_attachment=True)

app.run(host="0.0.0.0", port=5000)
